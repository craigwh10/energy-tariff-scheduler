from datetime import timezone, datetime
from typing import Callable, Optional, Type
from abc import abstractmethod, ABC
import logging

from prices import OctopusAgilePricesClient, Price

import schedule # https://github.com/dbader/schedule
from pydantic import BaseModel, ValidationError
from pydantic.types import PositiveInt


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
        """
        Define what to do when a price is considered cheap or expensive.
        
        Example
        ```python
        if price.value < 10 and position < 5:
            self.config.action_when_cheap(price)
        else:
            self.config.action_when_expensive(price)
        ```
        """
        pass

class ScheduleConfig(BaseModel):
    prices_to_include: PositiveInt | Callable[[list[Price]], int]
    action_when_cheap: Callable[[Optional[Price]], None]
    action_when_expensive: Callable[[Optional[Price]], None]
    # this allows people to simply pass in a class, rather than an instance
    _pricing_strategy: Optional[PricingStrategy] = None

    def add_custom_pricing_strategy(self, pricing_strategy: Type[PricingStrategy]):
        """
        Adds a custom pricing strategy to the configuration.
        You pass in a class, not an instance as the config is injected later.
        ```
        """
        # it's done this way to allow for the custom strategy to access the config
        if not issubclass(pricing_strategy, PricingStrategy):
            raise Exception(f"The custom pricing strategy {pricing_strategy.__name__} must inherit from PricingStrategy\nException fix: use 'from schedules import PricingStrategy' and 'class {pricing_strategy.__name__}(PricingStrategy):'")

        try:
            instance = pricing_strategy(self)
            # accessing this will raise if it's not implemented
            # it doesn't need a raise NotImplemented within the method, ABC throws by default if
            # it's not implemented as TypeError
            instance.handle_price  
        except TypeError:
            raise Exception("The 'handle_price' method must be implemented in the custom pricing strategy")
        
        self._pricing_strategy = pricing_strategy

        return self
    
    model_config = dict(
        # this allows people to pass in extra fields,
        # *primarily for pricing strategy*
        extra="forbid"
    )


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

        time = price.datetime_from.strftime("%H:%M")

        if (sorted_position <= number_of_cheapest_to_include - 1):
            logging.info(f"Time: {time}, Action: action_when_cheap, Price: {price.value}p/kWh")
            self.config.action_when_cheap(price)
        if (sorted_position > number_of_cheapest_to_include - 1):
            logging.info(f"Time: {time}, Action: action_when_expensive, Price: {price.value}p/kWh")
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

        logging.info(f"Generating schedule for {len(todays_prices)} prices")
        for price in todays_prices:
            if price.datetime_from < datetime.now(timezone.utc):
                logging.warning(f"Skipping price {price} as it's in the past")
                continue

            def job(price: Price):
                def schedule_price_task():
                    if self.config._pricing_strategy is None:
                        pricing_strategy = DefaultPricingStrategy(self.config)
                        pricing_strategy.handle_price(price=price, prices=todays_prices)

                    else:
                        pricing_strategy = self.config._pricing_strategy(self.config)
                        pricing_strategy.handle_price(price=price, prices=todays_prices)
                    
                    # only run once for this set of prices
                    return schedule.CancelJob
            
                return schedule_price_task

            job_to_run = job(price)
            time_to_run = price.datetime_from.strftime("%H:%M")
            date_running_on = price.datetime_from.strftime("%d/%m/%Y %H:%M")

            # TODO: I can forsee people possibly want to do jobs within these half hourly blocks
            #       but this should be a future feature on request.
            schedule.every().day.at(time_to_run).do(job_to_run).tag(f"{date_running_on}")

        logging.info("Schedule generated, waiting for jobs to run...")
