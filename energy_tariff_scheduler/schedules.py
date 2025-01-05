from typing import Callable
from abc import abstractmethod, ABC
import logging
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from .prices import OctopusPricesClient, Price

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Resolves circular import as it's only used
    # for typing.
    from .config import OctopusAgileScheduleConfig, OctopusGoScheduleConfig
    from .config import TrackedScheduleConfigCreator, CompleteConfig

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
    """
    Simply determines if the price is within the cheapest prices to include and runs the appropriate action.
    """
    def __init__(self, config: "CompleteConfig"):
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

class OctopusGoScheduleProvider(ScheduleProvider):
    def __init__(
            self,
            prices_client: OctopusPricesClient,
            config: "OctopusGoScheduleConfig",
            scheduler: BackgroundScheduler,
            tracked_schedule_config: "TrackedScheduleConfigCreator"
        ):
        self.prices_client = prices_client
        self.scheduler = scheduler
        self.tracked_schedule_config = tracked_schedule_config
        self.config = config

    def run(self):
        today_date = datetime.now(timezone.utc)

        date_from = (datetime(
            hour=0,
            minute=0,
            year=today_date.year,
            month=today_date.month,
            day=today_date.day
        )).isoformat("T")

        date_to = datetime(
            hour=0,
            minute=0,
            year=today_date.year,
            month=today_date.month,
            day=today_date.day + 1    
        ).isoformat("T")

        product_prefix = "INTELLI" if self.config.is_intelligent == True else "GO"

        todays_prices = self.prices_client.get_prices_for_users_tariff_and_product(
            product_prefix=product_prefix, date_from=date_from, date_to=date_to
        )

        logging.info(f"Generating schedule for {len(todays_prices)} prices")

        pricing_strategy_class = self.config._pricing_strategy or DefaultPricingStrategy

        for price in todays_prices:
            pricing_strategy_class(self.tracked_schedule_config.get_config()).handle_price(price, prices=todays_prices)

            def job(price: Price):
                def run_price_task():
                    pricing_strategy_class(self.config).handle_price(price, prices=todays_prices)
                    
                return run_price_task

            active_job_run_dates = [job.next_run_time for job in self.scheduler.get_jobs()]

            logging.debug(active_job_run_dates)
            if price.datetime_from in active_job_run_dates:
                """
                This covers when you run it first time, it makes 3 jobs:
                - yesterdays hangover price (cheap if intel, expensive if go)
                - todays cheapest period (for go)
                - todays expensive period (for go and intel)
                - today and tomorrows expensive period (for go)
                Doing this we don't try recreating a job that goes into tomorrow.
                """
                logging.info(f"not adding job {price.datetime_from} as it already exists")
                continue

            logging.debug(f"Added new job for {price.datetime_from}")

            self.scheduler.add_job(
                func=job(price),
                trigger='date',
                run_date=price.datetime_from.replace(tzinfo=ZoneInfo("GMT")),
                misfire_grace_time=60*10,
                next_run_time=price.datetime_from.replace(tzinfo=ZoneInfo("GMT")),
            )

        logging.info("Schedule generated")


class OctopusAgileScheduleProvider(ScheduleProvider):
    def __init__(
            self,
            prices_client: OctopusPricesClient,
            config: "OctopusAgileScheduleConfig",
            scheduler: BackgroundScheduler,
            tracked_schedule_config: "TrackedScheduleConfigCreator"
        ):
        self.prices_client = prices_client
        self.config = config
        self.scheduler = scheduler
        self.tracked_schedule_config = tracked_schedule_config

    def run(self):
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

        todays_prices = self.prices_client.get_prices_for_users_tariff_and_product("AGILE", date_from, date_to)

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
                run_date=price.datetime_from.replace(tzinfo=ZoneInfo("GMT")),
                misfire_grace_time=60*15,
                next_run_time=price.datetime_from.replace(tzinfo=ZoneInfo("GMT"))
            )
    
        logging.info("Schedule generated")
