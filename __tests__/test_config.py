from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
import time_machine

from config import ScheduleConfig
from prices import Price
from schedules import PricingStrategy

"""

"""

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

        def mock_spec(price):
            return ''

        action_when_cheap = mocker.create_autospec(mock_spec)
        action_when_cheap.__name__ = "action_when_cheap"
        action_when_expensive = mocker.create_autospec(mock_spec)
        action_when_expensive.__name__ = "action_when_cheap"

        class InvalidCustomPricingStrategy:
            def __init__(self, config: ScheduleConfig):
                self.config = config
            def handle_price(self, price: Price, position: int, prices: list[Price]):
                if price.value < 5.0:
                    self.config.action_when_cheap(price)
                else:
                    self.config.action_when_expensive(price)

        with pytest.raises(
                SystemExit,
            ):
            ScheduleConfig(
                prices_to_include=2,
                action_when_cheap=action_when_cheap,
                action_when_expensive=action_when_expensive,
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

        def mock_spec(price):
            return ''

        action_when_cheap = mocker.create_autospec(mock_spec)
        action_when_cheap.__name__ = "action_when_cheap"
        action_when_expensive = mocker.create_autospec(mock_spec)
        action_when_expensive.__name__ = "action_when_cheap"

        class InvalidCustomPricingStrategy(PricingStrategy):
            def __init__(self, config: ScheduleConfig):
                self.config = config
            def handle_priceINVALID(self, price: Price, prices: list[Price]):
                if price.value < 5.0:
                    self.config.action_when_cheap(price)
                else:
                    self.config.action_when_expensive(price)

        with pytest.raises(
                SystemExit,
            ):
            ScheduleConfig(
                prices_to_include=2,
                action_when_cheap=action_when_cheap,
                action_when_expensive=action_when_expensive,
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

        def mock_spec(price):
            return ''

        action_when_cheap = mocker.create_autospec(mock_spec)
        action_when_cheap.__name__ = "action_when_cheap"
        action_when_expensive = mocker.create_autospec(mock_spec)
        action_when_expensive.__name__ = "action_when_cheap"

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
            ScheduleConfig(
                prices_to_include=2,
                action_when_cheap=action_when_cheap,
                action_when_expensive=action_when_expensive,
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

        def mock_spec(price):
            return ''

        action_when_cheap = mocker.create_autospec(mock_spec)
        action_when_cheap.__name__ = "action_when_cheap"
        action_when_expensive = mocker.create_autospec(mock_spec)
        action_when_expensive.__name__ = "action_when_cheap"

        class InvalidCustomPricingStrategy(PricingStrategy):
            def __init__(self, config: ScheduleConfig):
                self.config = config
            def handle_price(self):
                pass

        with pytest.raises(
                SystemExit,
            ):
            ScheduleConfig(
                prices_to_include=2,
                action_when_cheap=action_when_cheap,
                action_when_expensive=action_when_expensive,
            ).add_custom_pricing_strategy(InvalidCustomPricingStrategy)