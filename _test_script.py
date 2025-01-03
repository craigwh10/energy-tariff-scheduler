import logging
import requests

from energy_tariff_scheduler import Price, runner
from dotenv import load_dotenv
import os

OCTO_ACC_NO = os.getenv('OCTO_ACC_NO')
OCTO_API_KEY = os.getenv('OCTO_API_KEY')

load_dotenv()

logging.getLogger().setLevel(logging.DEBUG)

logging.debug("starting")

def switch_shelly_on_and_alert(price: Price):
    logging.info(f"Price is cheap: {price}")
    requests.get("http://192.168.1.235/relay/0?turn=on")

def switch_shelly_off_and_alert(price: Price):
    logging.info(f"Price is expensive: {price}")
    requests.get("http://192.168.1.235/relay/0?turn=off")

runner.run_octopus_agile_tariff_schedule(
    prices_to_include=10,
    action_when_cheap=switch_shelly_on_and_alert,
    action_when_expensive=switch_shelly_off_and_alert,
    api_key=OCTO_API_KEY,
    account_number=OCTO_ACC_NO
)