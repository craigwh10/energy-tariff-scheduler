import logging
import requests
from abc import ABC, abstractmethod
from pydantic import BaseModel
from datetime import timezone, datetime

class Price(BaseModel):
    value: float
    datetime_from: datetime
    datetime_to: datetime

class PricesClient(ABC):
    @abstractmethod
    def get_today(self) -> list[Price]:
        pass

class OctopusAgilePricesClient(PricesClient):
    def get_today():
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
        if (today_date.hour > 1):
            logging.warning("data includes historical prices, these wont be included in todays run.")

        data = requests.get(
            f"https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-C/standard-unit-rates/?period_from={date_from}&period_to={date_to}"
        )
        
        logging.debug("Price data", data.json())

        if data.json()["results"] == None:
            raise Exception("No data returned from the Octopus API so can't generate schedule, try running this again in a few minutes.")

        if len(data.json()["results"]) != 46:
            logging.warning("Data is incomplete, not all usual half hourly periods are included")
            logging.warning("This is likely a problem with the Octopus API, try running this again in a few minutes")
            logging.warning("If you believe this isn't an issue with the API then raise an issue here https://github.com/craigwh10/domestic-tariff-scheduler-sdk/issues/new.")

        return [Price(
            price=float(hh_period["value_inc_vat"]),
            datetime_from=datetime().fromisoformat(hh_period["valid_from"]).replace(tzinfo=timezone.utc),
            datetime_to=datetime().fromisoformat(hh_period["valid_to"]).replace(tzinfo=timezone.utc)
        ) for hh_period in data.json()["results"]]