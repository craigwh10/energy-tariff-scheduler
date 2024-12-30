from schedules import OctopusAgileScheduleProvider, ScheduleConfig, PricingStrategy
from prices import OctopusAgilePricesClient, Price

from typing import Callable, Optional, Type
import time
from datetime import datetime, timezone

import schedule

"""
Current tariff support:
- [Octopus Agile](https://octopus.energy/smart/agile/)
"""

def run_octopus_agile_tariff_schedule(
        prices_to_include: int | Callable[[list[Price]], int],
        action_when_cheap: Callable[[Optional[Price]], None],
        action_when_expensive: Callable[[Optional[Price]], None],
        pricing_strategy: Optional[Type[PricingStrategy]] = None,
        run_continously: bool = True
    ):
    """
    Runs a schedule with half hourly jobs based on the Octopus Agile tariff prices.
    
    Args:
        prices_to_include: The number of prices to include or a callable that determines the number dynamically from available prices.
        action_when_cheap: Action to execute when the price is considered cheap.
        action_when_expensive: Action to execute when the price is considered expensive.
        pricing_strategy: Custom pricing strategy to handle the prices.

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
                prices_to_include,
                action_when_cheap,
                action_when_expensive,
            ).add_custom_pricing_strategy(pricing_strategy)
        ).run()

    if run_continously:
        if not datetime.now(tz=timezone.utc).hour == 0:
            run_new_schedule()

        schedule.every().day.at("00:00").do(run_new_schedule)
        while 1:
            schedule.run_pending()
            time.sleep(1)

    if not run_continously:
        # only runs 
       run_new_schedule()
       while 1:
        schedule.run_pending()
        time.sleep(1)

        if datetime.now(tz=timezone.utc).hour == 0:
            exit(1)
    
