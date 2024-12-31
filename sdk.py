from schedules import DefaultPricingStrategy, OctopusAgileScheduleProvider, ScheduleConfig, PricingStrategy
from prices import OctopusAgilePricesClient, Price

from typing import Callable, Optional, Type
import time
from datetime import datetime, timezone
import logging

import schedule

"""
Current tariff support:
- [Octopus Agile](https://octopus.energy/smart/agile/)
"""

def run_octopus_agile_tariff_schedule(
        prices_to_include: int | Callable[[list[Price]], int],
        action_when_cheap: Callable[[Optional[Price]], None],
        action_when_expensive: Callable[[Optional[Price]], None],
        pricing_strategy: Optional[Type[PricingStrategy]] = DefaultPricingStrategy,
        run_continously: bool = True
    ):
    """
    Runs a schedule with half hourly jobs based on the Octopus Agile tariff prices.
    
    Args:
        prices_to_include: The number of prices to include or a callable that determines the number dynamically from available prices.
        action_when_cheap: Action to execute when the price is considered cheap.
        action_when_expensive: Action to execute when the price is considered expensive.
        pricing_strategy: Custom pricing strategy to handle the prices.
        run_continously: Whether to run the schedule continuously (every day) or just once.
        
    Example Custom Pricing Strategy (Optional - default is just picking the cheapest `prices_to_include` prices):
    ```python
    from custom_sms import SMS
    import requests
    import logging
    from DomesticTariffSchedulerSDK import PricingStrategy, Price

    class CustomPricingStrategy(PricingStrategy):
        def __init__(self, config: ScheduleConfig):
            self.config = config # for access to other set configuration

        def _get_carbon_intensity(self, price: Price):
            res = requests.get(f"https://api.carbonintensity.org.uk/intensity/{price.datetime_from}")
            return res.json()["data"][0]["intensity"]["actual"]

        def handle_price(self, price: Price, prices: list[Price]):
            if price.value < 5 and self._get_carbon_intensity(price) < 100:
                self.config.action_when_cheap(price)
            else:
                self.config.action_when_expensive(price)

    def switch_shelly_on_and_alert(price: Price):
        logging.info(f"Price is cheap: {price}")
        SMS.send(f"Price is cheap ({price}p/kWh), turning on shelly")
        requests.get("http://<shelly_ip>/relay/0?turn=on")

    def switch_shelly_off_and_alert(price: Price):
        logging.info(f"Price is expensive: {price}")
        SMS.send(f"Price is expensive ({price}p/kWh), turning off shelly")    
        requests.get("http://<shelly_ip>/relay/0?turn=off")

    sdk = DomesticTariffSchedulerSDK.run_octopus_agile_tariff_schedule(
        prices_to_include=5, # 5 opportunties to trigger "action_when_cheap"
        action_when_cheap=switch_shelly_on_and_alert,
        action_when_expensive=switch_shelly_off_and_alert,
        pricing_strategy=CustomPricingStrategy
    )
    ```
    """
    def run_new_schedule():
        return OctopusAgileScheduleProvider(
            prices_client=OctopusAgilePricesClient(),
            config=ScheduleConfig(
                prices_to_include=prices_to_include,
                action_when_cheap=action_when_cheap,
                action_when_expensive=action_when_expensive,
            ).add_custom_pricing_strategy(pricing_strategy)
        ).run()
    
    def handle_running_at_exactly00(now: datetime):
        # This is actually a problem at every single time you run it on
        # but 00:00 is the automated run time so we'll just handle it here
        if (
            now.hour == 0 and 
            now.minute >= 0 and 
            now.minute < 30
        ):
            jobs = schedule.get_jobs()
            jobs_iter = list(jobs)
            problematic_jobs = [job for job in jobs_iter if job.at_time.strftime("%H:%M:%S") == "00:00:00"]
            
            if len(problematic_jobs) > 0:
                for problematic_job in problematic_jobs:
                    if "new_schedule" not in problematic_job.tags:
                        problematic_job.run() # annoyingly this reschedules it again...
                        schedule.cancel_job(problematic_job)
                        logging.debug(f"problematic job ran and cancelled")

    now = datetime.now(tz=timezone.utc)

    if run_continously == True:
        ran_00_check = False
        first_schedule_ran = False

        run_new_schedule()

        while True:
            # after first run finished, set the new repeating schedule
            if (
                datetime.now(tz=timezone.utc).hour == 23 and
                datetime.now(tz=timezone.utc).minute == 30 and
                first_schedule_ran == False
            ):
                first_schedule_ran = True
                schedule.every().day.at("00:00").do(run_new_schedule).tag("new_schedule")
                logging.debug(f"set recurring schedule")
            
            if (ran_00_check == False and now.hour == 0):
                # this only runs on first schedule where its possible to immediately start on 00:00
                handle_running_at_exactly00(now)
                ran_00_check = True

            jobs = schedule.get_jobs()

            logging.info(f"Jobs remaining this schedule: {len(jobs)}")

            if len(jobs) == 2:
                for job in jobs:
                    logging.debug(f"<remainder> {job.tags} :: {job}")

            schedule.run_pending()
            time.sleep(1)

    if run_continously == False:
       run_new_schedule()
       ran_00_check = False
       while True:
        jobs = schedule.get_jobs()

        logging.info(f"Jobs remaining this schedule: {len(jobs)}")
        if not ran_00_check: # prevent race conditions if check takes longer than 1s
            handle_running_at_exactly00(now)
        ran_00_check = True 

        schedule.run_pending()
        time.sleep(1)

        if len(jobs) == 0:
            exit(1)
    
