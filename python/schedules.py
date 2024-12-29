from datetime import timezone, datetime
from typing import Callable, Optional
from abc import abstractmethod, ABC

from prices import OctopusAgilePricesClient, Price

import schedule # https://github.com/dbader/schedule
from pydantic import BaseModel


class ScheduleProvider(ABC):
    @abstractmethod
    def run(self):
        pass


class PricingStrategy(ABC):
    """
    Contract for pre-defined or user defined price handling strategies.
    -
    This determines what logic should run at each half hourly period.
    """
    @abstractmethod
    def handle_price(self, price: Price, position: int, prices: list[Price]):
        """Define what to do when a price is considered cheap."""
        pass


class ScheduleConfig(BaseModel):
    prices_to_include: int | Callable[[list[Price]], int]
    action_when_cheap: Callable[[Optional[Price]], None]
    action_when_expensive: Callable[[Optional[Price]], None]
    pricing_strategy: Optional[PricingStrategy]


class DefaultPricingStrategy(PricingStrategy):
    def __init__(self, config: ScheduleConfig):
        self.config = config

    def _determine_cheapest_to_include(self, prices):
        if isinstance(self.config.prices_to_include, Callable):
            number_of_cheapest_to_include = self.config.prices_to_include(prices)

        if isinstance(self.config.prices_to_include, int):
            number_of_cheapest_to_include = self.config.prices_to_include
        
        return number_of_cheapest_to_include

    def handle_price(self, price: Price, prices: list[Price]):
        sorted_prices = sorted(prices, key=lambda obj: min(obj.value, obj.value))
        sorted_position = sorted_prices.index(price)

        number_of_cheapest_to_include = self._determine_cheapest_to_include(prices)

        if (sorted_position <= number_of_cheapest_to_include):
            self.config.action_when_cheap(price)
        if (sorted_position > number_of_cheapest_to_include):
            self.config.action_when_expensive(price)
        

class OctopusAgileScheduleProvider(ScheduleProvider):
    def __init__(self, prices_client: OctopusAgilePricesClient, config: ScheduleConfig):
        self.prices_client = prices_client
        self.config = config

    def run(self):
        """
        Triggers the half hourly schedule based on the users configuration based on the Octopus Agile prices for the day
        """
        todays_prices = self.prices_client.get_today()

        for price in todays_prices:
            if price.datetime_from < datetime.now(timezone.utc):
                continue

            def job(price: Price):
                def run():
                    if self.config.pricing_strategy is None:
                        pricing_strategy = DefaultPricingStrategy(self.config)
                        pricing_strategy.handle_price(price=price, prices=todays_prices)

                    else:
                        pricing_strategy = self.config.pricing_strategy(self.config)
                        pricing_strategy.handle_price(price=price, prices=todays_prices)
                    
                    # only run once for this set of prices
                    return schedule.CancelJob
            
                return run

            job_to_run = job(price)
            time_to_run = price.datetime_from.strftime("%H:%M")

            # TODO: I can forsee people possibly want to do jobs within these half hourly blocks
            #       but this should be a future feature on request.
            schedule.every().day.at(time_to_run).do(job_to_run)
