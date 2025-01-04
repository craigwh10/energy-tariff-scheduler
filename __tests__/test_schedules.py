from datetime import datetime

import sys
import os
from datetime import timezone
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from pytest_mock import MockerFixture
import time_machine

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../energy_tariff_scheduler/')) 
sys.path.insert(0, module_dir)

from energy_tariff_scheduler.schedules import PricingStrategy, DefaultPricingStrategy, OctopusAgileScheduleProvider, OctopusGoScheduleProvider
from unittest.mock import Mock
from energy_tariff_scheduler.config import CompleteConfig
from energy_tariff_scheduler.prices import Price

class TestDefaultPricingStrategy:
    def test_happy_path_with_int_cheapest_prices_to_include(self):
        class MockConfig:
            prices_to_include = 2
            action_when_cheap = Mock()
            action_when_expensive = Mock()

        mock_config = MockConfig()
 
        strategy = DefaultPricingStrategy(mock_config)
        strategy.handle_price(
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30),datetime_to=datetime(2024, 3, 24, 1, 0)),
            [
                Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30), datetime_to=datetime(2024, 3, 24, 1, 0)),
                Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0), datetime_to=datetime(2024, 3, 24, 1, 30)),
                Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30), datetime_to=datetime(2024, 3, 24, 2, 0)),
                Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0), datetime_to=datetime(2024, 3, 24, 2, 30))
            ]
        )

        mock_config.action_when_cheap.assert_not_called()
        mock_config.action_when_expensive.assert_called_once()
    
    def test_happy_path_with_callable_cheapest_prices_to_include(self):
        def _prices_to_include(prices):
            # only get the count where sum cost is no greater than 15p/kWh
            # e.g 3.0 + 5.0 + 3.0 + 4.0 = 15 (wont include 8.0)

            total = 0
            count = 0
            sorted_prices = sorted(prices, key=lambda obj: min(obj.value, obj.value))
            for price in sorted_prices:
                total += price.value
                count += 1
                if total >= 15:
                    break 

            return count

        class MockConfig:
            # workaround: https://stackoverflow.com/a/35322635
            prices_to_include = staticmethod(_prices_to_include)
            action_when_cheap = Mock()
            action_when_expensive = Mock()

        mock_config = MockConfig()
 
        strategy = DefaultPricingStrategy(mock_config)
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

        mock_config.action_when_expensive.assert_called_once()

    def test_handles_price_include_length_greater_than_prices(self):
        class MockConfig:
            prices_to_include = 6
            action_when_cheap = Mock()
            action_when_expensive = Mock()
            _pricing_strategy = None

        mock_config = MockConfig()
 
        strategy = DefaultPricingStrategy(mock_config)
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

        mock_config.action_when_cheap.assert_called_once()

class TestOctopusAgileScheduleProvider:
    @time_machine.travel(datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc))
    def test_happy_path(self, mocker: MockerFixture):
        mock_prices_client = Mock()
        mock_prices_client.get_prices_for_users_tariff_and_product.return_value = [
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc)),
            Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc)),
            Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 3, 0, tzinfo=timezone.utc))
        ]

        class MockConfig:
            prices_to_include = 2
            action_when_cheap = Mock()
            action_when_expensive = Mock()
            _pricing_strategy = None

        mock_schedule = mocker.MagicMock()
        mock_function = mocker.MagicMock(return_value="mocked result")
        
        mock_config = MockConfig()
        
        mock_tracker_config = mocker.MagicMock()
        mock_tracker_config.get_config.return_value = mock_config

        mock_schedule.add_job = mock_function

        provider = OctopusAgileScheduleProvider(
            mock_prices_client, mock_config, mock_schedule, mock_tracker_config
        )

        provider.run()
    
        assert mock_function.call_count == 5

    @time_machine.travel(datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc))
    def test_happy_path_with_custom_pricing_strategy(self, mocker: MockerFixture):
        mock_prices_client = Mock()
        mock_prices_client.get_prices_for_users_tariff_and_product.return_value = [
            Price(value=8.0, datetime_from=datetime(2024, 3, 24, 0, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc)),
            Price(value=4.0, datetime_from=datetime(2024, 3, 24, 1, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 1, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc)),
            Price(value=5.0, datetime_from=datetime(2024, 3, 24, 2, 0, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc)),
            Price(value=3.0, datetime_from=datetime(2024, 3, 24, 2, 30, tzinfo=timezone.utc),datetime_to=datetime(2024, 3, 24, 3, 0, tzinfo=timezone.utc))
        ]

        class CustomPricingStrategy(PricingStrategy):
            def __init__(self, config: CompleteConfig):
                self.config = config
            def handle_price(self, price: Price, prices: list[Price]):
                if price.value < 5.0:
                    self.config.action_when_cheap(price)
                else:
                    self.config.action_when_expensive(price)

        class MockConfig:
            prices_to_include = 2
            action_when_cheap = Mock()
            action_when_expensive = Mock()
            pricing_strategy = CustomPricingStrategy
            _pricing_strategy = None

        mock_config = MockConfig()

        mock_schedule = mocker.MagicMock()
        mock_function = mocker.MagicMock(return_value="mocked result")

        mock_schedule.add_job = mock_function

        mock_tracker_config = mocker.MagicMock()
        mock_tracker_config.get_config.return_value = mock_config

        provider = OctopusAgileScheduleProvider(
            mock_prices_client, mock_config, mock_schedule, mock_tracker_config
        )
        provider.run()
    
        assert mock_schedule.add_job.call_count == 5
    
class TestOctopusGoScheduleProvider:
    @time_machine.travel(datetime(2025, 1, 4, 0, 0, tzinfo=timezone.utc))
    def test_non_intelligent_run(self, mocker: MockerFixture):
        mock_prices_client = Mock()
        mock_prices_client.get_prices_for_users_tariff_and_product.return_value = [
            Price(
                value=27,
                datetime_from=datetime(2025, 1, 4, 5, 30, tzinfo=timezone.utc),
                datetime_to=datetime(2025, 1, 5, 0, 30, tzinfo=timezone.utc)),
            Price(
                value=6,
                datetime_from=datetime(2025, 1, 4, 0, 30, tzinfo=timezone.utc),
                datetime_to=datetime(2025, 1, 4, 5, 30, tzinfo=timezone.utc)
            ),
            Price(
                value=27,
                datetime_from=datetime(2025, 1, 3, 5, 30, tzinfo=timezone.utc),
                datetime_to=datetime(2025, 1, 4, 0, 30, tzinfo=timezone.utc)
            ),
        ]

        class MockConfig:
            is_intelligent = False
            prices_to_include = 2
            action_when_cheap = Mock()
            action_when_expensive = Mock()
            _pricing_strategy = None

        mock_schedule = mocker.MagicMock()
        mock_add_job = mocker.MagicMock(return_value="mocked result")

        mock_config = MockConfig()
        
        mock_tracker_config = mocker.MagicMock()
        mock_tracker_config.get_config.return_value = mock_config

        mock_schedule.add_job = mock_add_job

        provider = OctopusGoScheduleProvider(
            mock_prices_client, mock_config, mock_schedule, mock_tracker_config
        )

        provider.run()
    
        # should only generate a day of 15 min schedules 
        assert mock_add_job.call_args_list[0][1]['run_date'] == datetime(2025, 1, 4, 0, 0, tzinfo=ZoneInfo("GMT"))
        assert mock_add_job.call_args_list[-1][1]['run_date'] == datetime(2025, 1, 4, 23, 45, tzinfo=ZoneInfo("GMT"))

    @time_machine.travel(datetime(2025, 1, 4, 0, 0, tzinfo=timezone.utc))
    def test_intelligent_run(self, mocker: MockerFixture):
        mock_prices_client = Mock()
        mock_prices_client.get_prices_for_users_tariff_and_product.return_value = [
            Price(
                value=7.0,
                datetime_from=datetime(2025, 1, 4, 23, 30, tzinfo=timezone.utc),
                datetime_to=datetime(2025, 1, 5, 5, 30, tzinfo=timezone.utc)),
            Price(
                value=43.0,
                datetime_from=datetime(2025, 1, 4, 5, 30, tzinfo=timezone.utc),
                datetime_to=datetime(2025, 1, 4, 23, 30, tzinfo=timezone.utc)
            ),
            Price(
                value=7.0,
                datetime_from=datetime(2025, 1, 3, 23, 30, tzinfo=timezone.utc),
                datetime_to=datetime(2025, 1, 4, 5, 30, tzinfo=timezone.utc)
            ),
        ]

        class MockConfig:
            is_intelligent = True
            prices_to_include = 2
            action_when_cheap = Mock()
            action_when_expensive = Mock()
            _pricing_strategy = None

        mock_schedule = mocker.MagicMock()
        mock_add_job = mocker.MagicMock(return_value="mocked result")

        mock_config = MockConfig()
        
        mock_tracker_config = mocker.MagicMock()
        mock_tracker_config.get_config.return_value = mock_config

        mock_schedule.add_job = mock_add_job

        provider = OctopusGoScheduleProvider(
            mock_prices_client, mock_config, mock_schedule, mock_tracker_config
        )

        provider.run()
    
        # should only generate a day of 15 min schedules 
        assert mock_add_job.call_args_list[0][1]['run_date'] == datetime(2025, 1, 4, 0, 0, tzinfo=ZoneInfo("GMT"))
        assert mock_add_job.call_args_list[-1][1]['run_date'] == datetime(2025, 1, 4, 23, 45, tzinfo=ZoneInfo("GMT"))
