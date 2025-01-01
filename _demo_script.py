import os
import sys
import logging

from energy_tariff_scheduler import PricingStrategy, Price, runner

logging.getLogger().setLevel(logging.DEBUG)

logging.debug("starting")

def switch_shelly_on_and_alert(price: Price):
    print("Switching Shelly on and alerting")

def switch_shelly_off_and_alert(price: Price):
    print("Switching Shelly off and alerting")

def custom_price(prices: list[Price]):
    return 2

class CustomPriceStrategy(PricingStrategy):
    def __init__(self, config):
        self.config = config
    
    def handle_price(self, price: Price, prices: list[Price]):
        return

runner.run_octopus_agile_tariff_schedule(
    prices_to_include=custom_price,
    action_when_cheap=switch_shelly_on_and_alert,
    action_when_expensive=switch_shelly_off_and_alert,
    pricing_strategy=CustomPriceStrategy
)