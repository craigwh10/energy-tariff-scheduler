from typing import Callable
from abc import abstractmethod, ABC
import logging

from .prices import OctopusAgilePricesClient, Price

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Resolves circular import as it's only used
    # for typing.
    from config import ScheduleConfig
    from config import TrackedScheduleConfigCreator

from apscheduler.schedulers.background import BackgroundScheduler

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
    def handle_price(self, price: Price, prices: list[Price]):
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

class DefaultPricingStrategy(PricingStrategy):
    def __init__(self, config: "ScheduleConfig"):
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

        if (sorted_position <= number_of_cheapest_to_include - 1):
            self.config.action_when_cheap(price)
        if (sorted_position > number_of_cheapest_to_include - 1):
            self.config.action_when_expensive(price)

class OctopusAgileScheduleProvider(ScheduleProvider):
    def __init__(
            self,
            prices_client: OctopusAgilePricesClient,
            config: "ScheduleConfig",
            scheduler: BackgroundScheduler,
            tracked_schedule_config: "TrackedScheduleConfigCreator"
        ):
        self.prices_client = prices_client
        self.config = config
        self.scheduler = scheduler
        self.tracked_schedule_config = tracked_schedule_config

    def run(self):
        """
        Triggers the half hourly schedule based on the users configuration based on the Octopus Agile prices for the day
        """
        todays_prices = self.prices_client.get_today()
        logging.info(f"Generating schedule for {len(todays_prices)} prices")

        pricing_strategy_class = self.config._pricing_strategy or DefaultPricingStrategy

        for price in todays_prices:
            pricing_strategy_class(self.tracked_schedule_config.get_config()).handle_price(price, todays_prices)

            def job(price: Price):
                def run_price_task():
                    pricing_strategy_class(self.config).handle_price(price, todays_prices)
                    
                return run_price_task

            logging.debug(f"Added new job for {price.datetime_from}")

            # TODO: I can forsee people possibly want to do jobs within these half hourly blocks
            #       but this should be a future feature on request.
            self.scheduler.add_job(
                func=job(price),
                trigger='date',
                run_date=price.datetime_from,
                misfire_grace_time=60*15
            )
    
        logging.info("Schedule generated")
        
