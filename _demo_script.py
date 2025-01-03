import logging

from energy_tariff_scheduler import PricingStrategy, Price, runner
from dotenv import load_dotenv
import os

OCTO_ACC_NO = os.getenv('OCTO_ACC_NO')
OCTO_API_KEY = os.getenv('OCTO_API_KEY')

load_dotenv()

logging.getLogger("energy_tariff_scheduler").setLevel(logging.INFO)

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
    pricing_strategy=CustomPriceStrategy,
    api_key=OCTO_API_KEY,
    account_number=OCTO_ACC_NO
)