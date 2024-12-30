from unittest.mock import Mock
from sdk import run_octopus_agile_tariff_schedule
import time_machine
import time
import threading
import json
from datetime import datetime

from zoneinfo import ZoneInfo
import os
import sys
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../')) 
sys.path.insert(0, module_dir)

london_tz = ZoneInfo("Europe/London")

class TestIntegrationRunOctopusAgileTariffSchedule:
    def test_happy_path_that_schedule_on_run_once_calls_appropriately(self, mocker):
        with time_machine.travel(datetime(2023, 12, 11, 0, 0, tzinfo=london_tz), tick=False) as traveller:
            mock_price_provider = mocker.patch('requests.get')
            mock_price_provider.return_value.status_code = 200
            with open("./__tests__/mock_full_octopus_data.json") as f:
                mock_price_provider.return_value.json.return_value = json.load(f)

            action_when_cheap = Mock()
            action_when_expensive = Mock()

            def run_schedule():
                run_octopus_agile_tariff_schedule(
                    prices_to_include=5,
                    action_when_cheap=action_when_cheap,
                    action_when_expensive=action_when_expensive,
                    run_continously=False  # Enable continuous running for the loop
                )

            # Start the run in a separate thread
            schedule_thread = threading.Thread(target=run_schedule, daemon=True)
            schedule_thread.start()

            for hour in range(24):
                for minute in [0, 30]:
                    traveller.move_to(datetime(2023, 12, 11, hour, minute, tzinfo=london_tz))
                    time.sleep(1)

            schedule_thread.join(timeout=1)

            assert action_when_cheap.call_count == 5
