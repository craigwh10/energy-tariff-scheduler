import logging
import requests
from abc import ABC, abstractmethod
from datetime import timezone, datetime

from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed

class Price(BaseModel):
    value: float
    datetime_from: datetime
    datetime_to: datetime

    def __str__(self):
        return f"(value={self.value}, from={self.datetime_from.isoformat()}, to={self.datetime_to.isoformat()})"

class PricesClient(ABC):
    @abstractmethod
    def get_today(self) -> list[Price]:
        pass

class OctopusAgilePricesClient(PricesClient):
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
    def _request(self, date_from: str, date_to: str) -> dict:
        """
        Some times the octopus API doesn't return data, this is a retryable function to try and get the data
        This isn't failsafe, as there could be a persistent issue, which I have seen before, even 6 hours later.
        """
        url = f"https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-C/standard-unit-rates/?period_from={date_from}&period_to={date_to}"
        response = requests.get(url)
        response.raise_for_status()

        data_json = response.json()

        logging.debug(f"Full Octopus Agile data: {data_json}")

        if data_json == None:
            raise ValueError("No data returned from the Octopus Agile API, this is an Octopus API issue, try re-running this in a few minutes")
        
        data_json_results = data_json.get("results")

        if data_json_results == None or len(data_json_results) == 0:
            raise ValueError("Empty or None results returned from the Octopus Agile API, this is an Octopus API issue, try re-running this in a few minutes")

        return data_json_results

    def get_today(self) -> list[Price]:
        """
        What this does
        ---
        - Gets todays data, in utc time order
        - Todays data is made available between 4-8pm the day before

        Example response
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
        date_from = (datetime(
            hour=0,
            year=today_date.year,
            month=today_date.month,
            day=today_date.day
        )).isoformat("T")

        date_to = datetime(
            hour=23,
            year=today_date.year,
            month=today_date.month,
            day=today_date.day      
        ).isoformat("T")

        logging.info(f"Getting price data from {date_from} to {date_to}")

        # If the time is after 1am, then the data includes historical prices
        if (today_date.hour >= 1):
            logging.warning(f"current hour is {today_date.hour}, data includes historical prices, these wont be included in todays run.")

        data_json_results = self._request(date_from, date_to)

        if len(data_json_results) != 46:
            logging.warning("Data is incomplete, not all usual half hourly periods are included")
            logging.warning("This is likely a problem with the Octopus API, try running this again in a few minutes")
            logging.warning("If you believe this isn't an issue with the API then raise an issue here https://github.com/craigwh10/energy-tariff-scheduler/issues/new.")

        return [Price(
            value=float(hh_period["value_inc_vat"]),
            datetime_from=datetime.fromisoformat(hh_period["valid_from"]).replace(tzinfo=timezone.utc),
            datetime_to=datetime.fromisoformat(hh_period["valid_to"]).replace(tzinfo=timezone.utc)
        ) for hh_period in data_json_results]