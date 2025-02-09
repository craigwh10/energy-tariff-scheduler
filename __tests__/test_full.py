import logging
import os
import sys
from datetime import datetime
import responses
from pytest import fixture
import json

from time_machine import travel

from energy_tariff_scheduler import runner, PricingStrategy, Price

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../energy_tariff_scheduler/')) 
sys.path.insert(0, module_dir)

class TestFull:
    @responses.activate
    @travel(datetime(year=2024, month=12, day=12, hour=23, minute=58), tick=True)
    def test_should_call(self):
        logging.getLogger("energy_tariff_scheduler").setLevel(logging.INFO)

        with open('./__tests__/account.json') as f:
            account_res = json.load(f)

        with open('./__tests__/prices.json') as f:
            prices_res = json.load(f)

        responses.add(
            responses.GET,
            'http://localhost:8080/v1/accounts/acc',
            json=account_res
        )

        responses.add(
            responses.GET,
            'http://localhost:8080/v1/products/',
            json=prices_res
        )

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
            considered_price_count=custom_price,
            action_when_cheap=switch_shelly_on_and_alert,
            action_when_expensive=switch_shelly_off_and_alert,
            pricing_strategy=CustomPriceStrategy,
            api_key="123",
            account_number="acc"
        )