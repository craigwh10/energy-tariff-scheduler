import logging
import requests
from requests.auth import HTTPBasicAuth

from datetime import timezone, datetime
from difflib import SequenceMatcher

from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import OctopusAPIAuthConfig

class Price(BaseModel):
    value: float
    datetime_from: datetime
    datetime_to: datetime

    def __str__(self):
        return f"(value={self.value}, from={self.datetime_from.isoformat()}, to={self.datetime_to.isoformat()})"

"""
NOTE: Currently my assumption is that this setup should be able to get the prices for any tariff for octopus, but the schedules aren't.
NOTE: This is still TBD as I don't fully know the data structures from complex tariffs and setups yet, primarily just homes with smart meters.
"""

class OctopusCurrentTariffAndProductClient:
    def __init__(self, auth_config: "OctopusAPIAuthConfig"):
        self.auth_config = auth_config

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
    def get_account(self) -> dict:
        url = f"https://api.octopus.energy/v1/accounts/{self.auth_config.account_number}/"
        
        logging.info(f"Getting account details for your account number")

        response = requests.get(url, auth=HTTPBasicAuth(self.auth_config.api_key, ""))
        response.raise_for_status()

        account_details = response.json()

        logging.debug(f"Account details found")

        # add pydantic validation here

        return account_details
    
    def get_accounts_tariff_and_matched_product_code(self, product_code_prefix: str) -> tuple[str, str]:
        """
        product_code_prefix: "AGILE" or "GO"
        """
        # it may be that for some accounts, the tariff code isn't agile, we should make the user aware that
        # this tariff isn't supported at the moment but they can request it
        account_details = self.get_account()

        properties = account_details.get("properties")
        property = properties[0]

        meter_points = property.get("electricity_meter_points")

        tariffs_active: list[str] = []
        for idx, meter_point in enumerate(meter_points):
            agreements = meter_point.get("agreements")
            
            logging.debug(f"Agreement [{idx}]: {agreements}")  

            datetime_now = datetime.now(timezone.utc)
            current_agreement_by_none = [agreement for agreement in agreements if agreement.get("valid_to") == None]
            current_agreement_by_future = [
                agreement for agreement in agreements
                if (
                    datetime.fromisoformat(agreement.get("valid_to")) > datetime_now 
                    if agreement.get("valid_to") is not None 
                    else None
                )
            ]

            if len(current_agreement_by_none) == 0 and len(current_agreement_by_future) == 0:
                raise SystemExit(
                    f"Unable to find an active agreement for your account, check that you have a tariff active with Octopus"
                )
            
            if len(current_agreement_by_none) >= 1 and len(current_agreement_by_future) >= 1:
                raise SystemExit(
                    f"Found multiple active agreements for a meter, this is unexpected, please raise this on https://github.com/craigwh10/energy-tariff-scheduler/discussions/new?category=api-issues to help us understand how this has happened"
                )
            
            current_active_agreement = next(checked_agreement for checked_agreement in [
                current_agreement_by_none,
                current_agreement_by_future
            ] if len(checked_agreement) == 1)[0]
            
            latest_tariff_code = current_active_agreement.get("tariff_code")

            tariffs_active.append(latest_tariff_code)

        matched_tariff = next((tariff for tariff in tariffs_active if tariff.find(product_code_prefix)), None)

        if matched_tariff == None:
            raise SystemExit(
                f"The tariff code you are on isn't supported by this script, please read https://craigwh10.github.io/energy-tariff-scheduler/common-problems/#possibly-common-octopus-the-runner-isnt-finding-my-tariff-or-product"    
            )

        logging.info(f"Latest tariff code: {latest_tariff_code}")

        product_code_for_tariff = f"{latest_tariff_code[5:-2]}"

        logging.info(f"Using product: {product_code_for_tariff} for active tariff code {latest_tariff_code}")

        return latest_tariff_code, product_code_for_tariff

class OctopusPricesClient:
    def __init__(self, auth_config: "OctopusAPIAuthConfig", tariff_and_product_client: "OctopusCurrentTariffAndProductClient"):
        self.auth_config = auth_config
        self.tariff_and_product_client = tariff_and_product_client

    def get_prices(self, product_code: str, tariff_code: str, period_from: str, period_to: str) -> list[dict]:
        url = f"https://api.octopus.energy/v1/products/{product_code}/electricity-tariffs/{tariff_code}/standard-unit-rates/?period_from={period_from}&period_to={period_to}"
        response = requests.get(url)

        if response.status_code == 404:
            raise SystemExit("The tariff code you are on isn't supported by this script, please read https://craigwh10.github.io/energy-tariff-scheduler/common-problems/#possibly-common-octopus-the-runner-isnt-finding-my-tariff-or-product")

        response.raise_for_status()

        data_json = response.json()

        logging.debug(f"Full Octopus Agile data: {data_json}")

        if data_json == None:
            raise ValueError("No data returned from the Octopus Agile API, this is an Octopus API issue, try re-running this in a few minutes")
        
        data_json_results = data_json.get("results")

        if data_json_results == None or len(data_json_results) == 0:
            raise ValueError("Empty or None results returned from the Octopus Agile API, this is an Octopus API issue, try re-running this in a few minutes")

        return data_json_results 

    def get_prices_for_users_tariff_and_product(self, product_prefix: str, date_from: datetime, date_to: datetime) -> list[Price]:
        """
        What this does
        ---
        - Gets your current tariff and product
        - Gets todays data for product and tariff, in utc time order
        - Maps to price objects
        
        API Behaviour: Todays data is made available between 4-8pm the day before

        API Example prices response:
        ---
        [{
        "value_exc_vat": 23.4,
        "value_inc_vat": 24.57,
        "valid_from": "2023-03-26T01:00:00Z",
        "valid_to": "2023-03-26T01:30:00Z",
        "payment_method": null
        }]
        """
        today_date = datetime.now(timezone.utc)

        logging.info(f"Getting price data from {date_from} to {date_to}")

        # If the time is after 1am, then the data includes historical prices
        if (today_date.hour >= 1):
            logging.warning(f"current hour is {today_date.hour}, data includes historical prices, these wont be included in todays run.")

        tariff_code, product_code = self.tariff_and_product_client.get_accounts_tariff_and_matched_product_code(product_code_prefix=product_prefix)

        data_json_results = self.get_prices(product_code, tariff_code, date_from, date_to)

        return [Price(
            value=float(hh_period["value_inc_vat"]),
            datetime_from=datetime.fromisoformat(hh_period["valid_from"]).replace(tzinfo=timezone.utc),
            datetime_to=datetime.fromisoformat(hh_period["valid_to"]).replace(tzinfo=timezone.utc)
        ) for hh_period in data_json_results]