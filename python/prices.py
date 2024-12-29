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

        # TODO: Add a warning here that if you run it earlier later than 1am then it will produce less output

        data = requests.get(
            f"https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-C/standard-unit-rates/?period_from={date_from}&period_to={date_to}"
        )

        # TODO: Add error handling here, and validation of correct length of final result
        logging.debug("Price data", data.json())

        return [Price(
            price=float(hh_period["value_inc_vat"]),
            datetime_from=datetime().fromisoformat(hh_period["valid_from"]).replace(tzinfo=timezone.utc),
            datetime_to=datetime().fromisoformat(hh_period["valid_to"]).replace(tzinfo=timezone.utc)
        ) for hh_period in data.json()["results"]]