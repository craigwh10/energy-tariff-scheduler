from datetime import datetime, timezone
from unittest.mock import Mock
import os
import sys

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../energy_tariff_scheduler/')) 
sys.path.insert(0, module_dir)

print(sys.path)

import pytest
import time_machine

from energy_tariff_scheduler.config import CompleteConfig, PricingStrategyConfig
from energy_tariff_scheduler.prices import Price
from energy_tariff_scheduler.schedules import PricingStrategy



class TestScheduleConfig:
    @time_machine.travel(datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc))
    def test_invalid_inheritence_custom_pricing_strategy(self, mocker):
        mock_prices_client = Mock()
        mock_prices_client.get_today.return_value = [
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc)),
            Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc)),
            Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 3, 0, tzinfo=timezone.utc))
        ]


        class InvalidCustomPricingStrategy:
            def __init__(self, config: CompleteConfig):
                self.config = config
            def handle_price(self, price: Price, position: int, prices: list[Price]):
                if price.value < 5.0:
                    self.config.action_when_cheap(price)
                else:
                    self.config.action_when_expensive(price)

        with pytest.raises(
                SystemExit,
            ):
            PricingStrategyConfig(
            ).add_custom_pricing_strategy(InvalidCustomPricingStrategy)

    @time_machine.travel(datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc))
    def test_invalid_method_custom_pricing_strategy(self, mocker):
        mock_prices_client = Mock()
        mock_prices_client.get_today.return_value = [
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc)),
            Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc)),
            Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 3, 0, tzinfo=timezone.utc))
        ]

        class InvalidCustomPricingStrategy(PricingStrategy):
            def __init__(self, config: CompleteConfig):
                self.config = config
            def handle_priceINVALID(self, price: Price, prices: list[Price]):
                if price.value < 5.0:
                    self.config.action_when_cheap(price)
                else:
                    self.config.action_when_expensive(price)

        with pytest.raises(
                SystemExit,
            ):
            PricingStrategyConfig(
            ).add_custom_pricing_strategy(InvalidCustomPricingStrategy)

    @time_machine.travel(datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc))
    def test_invalid_init_custom_pricing_strategy(self, mocker):
        mock_prices_client = Mock()
        mock_prices_client.get_today.return_value = [
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc)),
            Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc)),
            Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 3, 0, tzinfo=timezone.utc))
        ]

        class InvalidCustomPricingStrategy(PricingStrategy):
            def __init__(self):
                pass
    
            def handle_price(self, price: Price, prices: list[Price]):
                if price.value < 5.0:
                    self.config.action_when_cheap(price)
                else:
                    self.config.action_when_expensive(price)

        with pytest.raises(
                SystemExit,
            ):
            PricingStrategyConfig(
            ).add_custom_pricing_strategy(InvalidCustomPricingStrategy)

    @time_machine.travel(datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc))
    def test_invalid_handle_price_too_little_params_custom_pricing_strategy(self, mocker):
        mock_prices_client = Mock()
        mock_prices_client.get_today.return_value = [
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc)),
            Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc)),
            Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 3, 0, tzinfo=timezone.utc))
        ]

        class InvalidCustomPricingStrategy(PricingStrategy):
            def __init__(self, config: CompleteConfig):
                self.config = config
            def handle_price(self):
                pass

        with pytest.raises(
                SystemExit,
            ):
            PricingStrategyConfig(
            ).add_custom_pricing_strategy(InvalidCustomPricingStrategy)