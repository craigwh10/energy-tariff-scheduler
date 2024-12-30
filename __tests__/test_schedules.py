from datetime import datetime

import sys
import os
from datetime import timezone

import pytest
import time_machine

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../')) 
sys.path.insert(0, module_dir)

from schedules import PricingStrategy, ScheduleConfig, DefaultPricingStrategy, OctopusAgileScheduleProvider
from unittest.mock import Mock
from prices import Price

class TestDefaultPricingStrategy:
    def test_happy_path_with_int_cheapest_prices_to_include(self):
        action_when_cheap = Mock()
        action_when_expensive = Mock()

        config = ScheduleConfig(
            prices_to_include=2,
            action_when_cheap=action_when_cheap,
            action_when_expensive=action_when_expensive,
        )
 
        strategy = DefaultPricingStrategy(config)
        strategy.handle_price(
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30),datetime_to=datetime(2024, 3, 24, 1, 0)),
            [
                Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30), datetime_to=datetime(2024, 3, 24, 1, 0)),
                Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0), datetime_to=datetime(2024, 3, 24, 1, 30)),
                Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30), datetime_to=datetime(2024, 3, 24, 2, 0)),
                Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0), datetime_to=datetime(2024, 3, 24, 2, 30))
            ]
        )

        action_when_cheap.assert_not_called()
        action_when_expensive.assert_called_once()
    
    def test_happy_path_with_callable_cheapest_prices_to_include(self):
        action_when_cheap = Mock()
        action_when_expensive = Mock()

        def prices_to_include(prices):
            # only get the count where sum cost is no greater than 15p/kWh
            # i.e 3.0 + 5.0 + 3.0 + 4.0 = 15 (wont include 8.0)

            total = 0
            count = 0
            sorted_prices = sorted(prices, key=lambda obj: min(obj.value, obj.value))
            for price in sorted_prices:
                total += price.value
                count += 1
                if total >= 15:
                    break 

            return count

        config = ScheduleConfig(
            prices_to_include=prices_to_include,
            action_when_cheap=action_when_cheap,
            action_when_expensive=action_when_expensive,
        )
 
        strategy = DefaultPricingStrategy(config)
        strategy.handle_price(
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30),datetime_to=datetime(2024, 3, 24, 1, 0)),
            [
                Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30), datetime_to=datetime(2024, 3, 24, 1, 0)),
                Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0), datetime_to=datetime(2024, 3, 24, 1, 30)),
                Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30), datetime_to=datetime(2024, 3, 24, 2, 0)),
                Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0), datetime_to=datetime(2024, 3, 24, 2, 30)),
                Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30), datetime_to=datetime(2024, 3, 24, 3, 0))
            ]
        )

        action_when_expensive.assert_called_once()

    def test_handles_price_include_length_greater_than_prices(self):
        action_when_cheap = Mock()
        action_when_expensive = Mock()

        config = ScheduleConfig(
            prices_to_include=6,
            action_when_cheap=action_when_cheap,
            action_when_expensive=action_when_expensive,
        )
 
        strategy = DefaultPricingStrategy(config)
        strategy.handle_price(
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30),datetime_to=datetime(2024, 3, 24, 1, 0)),
            [
                Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30), datetime_to=datetime(2024, 3, 24, 1, 0)),
                Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0), datetime_to=datetime(2024, 3, 24, 1, 30)),
                Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30), datetime_to=datetime(2024, 3, 24, 2, 0)),
                Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0), datetime_to=datetime(2024, 3, 24, 2, 30)),
                Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30), datetime_to=datetime(2024, 3, 24, 3, 0))
            ]
        )

        action_when_cheap.assert_called_once()

class TestOctopusAgileScheduleProvider:
    @time_machine.travel(datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc))
    def test_happy_path(self, mocker):
        mock_prices_client = Mock()
        mock_prices_client.get_today.return_value = [
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc)),
            Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc)),
            Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 3, 0, tzinfo=timezone.utc))
        ]

        action_when_cheap = Mock()
        action_when_expensive = Mock()

        config = ScheduleConfig(
            prices_to_include=2,
            action_when_cheap=action_when_cheap,
            action_when_expensive=action_when_expensive,
        )

        mock_schedule = mocker.patch('schedule.every')

        provider = OctopusAgileScheduleProvider(mock_prices_client, config)
        provider.run()
    
        assert mock_schedule.call_count == 5

    @time_machine.travel(datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc))
    def test_happy_path_with_custom_pricing_strategy(self, mocker):
        mock_prices_client = Mock()
        mock_prices_client.get_today.return_value = [
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc)),
            Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc)),
            Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 3, 0, tzinfo=timezone.utc))
        ]

        action_when_cheap = Mock()
        action_when_expensive = Mock()

        class CustomPricingStrategy(PricingStrategy):
            def __init__(self, config: ScheduleConfig):
                self.config = config
            def handle_price(self, price: Price, position: int, prices: list[Price]):
                if price.value < 5.0:
                    self.config.action_when_cheap(price)
                else:
                    self.config.action_when_expensive(price)

        config = ScheduleConfig(
            prices_to_include=2,
            action_when_cheap=action_when_cheap,
            action_when_expensive=action_when_expensive,
        ).add_custom_pricing_strategy(CustomPricingStrategy)

        mock_schedule = mocker.patch('schedule.every')

        provider = OctopusAgileScheduleProvider(mock_prices_client, config)
        provider.run()
    
        assert mock_schedule.call_count == 5

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

        action_when_cheap = Mock()
        action_when_expensive = Mock()

        class InvalidCustomPricingStrategy:
            def __init__(self, config: ScheduleConfig):
                self.config = config
            def handle_price(self, price: Price, position: int, prices: list[Price]):
                if price.value < 5.0:
                    self.config.action_when_cheap(price)
                else:
                    self.config.action_when_expensive(price)

        with pytest.raises(
                Exception,
                match="The custom pricing strategy InvalidCustomPricingStrategy must inherit from PricingStrategy\nException fix: use \'from schedules import PricingStrategy\' and \'class InvalidCustomPricingStrategy\(PricingStrategy\):\'"
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

        action_when_cheap = Mock()
        action_when_expensive = Mock()

        class InvalidCustomPricingStrategy(PricingStrategy):
            def __init__(self, config: ScheduleConfig):
                self.config = config
            def handle_priceINVALID(self, price: Price, position: int, prices: list[Price]):
                if price.value < 5.0:
                    self.config.action_when_cheap(price)
                else:
                    self.config.action_when_expensive(price)

        with pytest.raises(
                Exception,
                match="The \'handle_price\' method must be implemented in the custom pricing strategy"
            ):
            ScheduleConfig(
                prices_to_include=2,
                action_when_cheap=action_when_cheap,
                action_when_expensive=action_when_expensive,
            ).add_custom_pricing_strategy(InvalidCustomPricingStrategy)