# from unittest.mock import Mock
# from sdk import run_octopus_agile_tariff_schedule
# import time_machine
# import time
# import threading
# import json
# import pytest
# import schedule
# from datetime import datetime, timedelta
# import logging
# import __tests__.octopus_mock_data as octopus_mock_data

# from zoneinfo import ZoneInfo
# import os
# import sys
# module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../')) 
# sys.path.insert(0, module_dir)

# london_tz = ZoneInfo("Europe/London")

# class TestIntegrationRunOctopusAgileTariffSchedule:
#     @pytest.mark.skip()
#     def test_happy_path_that_schedule_on_run_once_calls_appropriately(self, mocker):
#         with time_machine.travel(datetime(2024, 12, 11, 0, 0, tzinfo=london_tz), tick=False) as traveller:
#             mock_price_provider = mocker.patch('requests.get')
#             mock_price_provider.return_value.status_code = 200
#             with open("./__tests__/mock_full_octopus_data.json") as f:
#                 mock_price_provider.return_value.json.return_value = json.load(f)

#             action_when_cheap = Mock()
#             action_when_expensive = Mock()

#             def run_schedule():
#                 with pytest.raises(SystemExit) as excinfo:
#                     run_octopus_agile_tariff_schedule(
#                         considered_price_count=5,
#                         action_when_cheap=action_when_cheap,
#                         action_when_expensive=action_when_expensive,
#                         run_continously=False  # Enable continuous running for the loop
#                     )
#                     assert excinfo.value.code == 1

#             # Start the run in a separate thread
#             schedule_thread = threading.Thread(target=run_schedule, daemon=True)
#             schedule_thread.start()

#             # for hour in range(24):
#             #     for minute in [0, 1, 2, 15, 30, 45]:
#             #         traveller.move_to(datetime(2023, 12, 11, hour, minute, tzinfo=london_tz))
#             #         time.sleep(1)

#             start_time = datetime.now()
#             end_time = start_time + timedelta(hours=23, minutes=30)

#             logging.debug(f"<TEST> Start time: {start_time}, End time: {end_time}")
#             while datetime.now() < end_time:
#                 traveller.shift(timedelta(minutes=15))
                
#                 logging.debug(f"<TEST> Simulated time: {datetime.now()}")
#                 time.sleep(0.05) # Simulates the schedule clock

#             schedule_thread.join(timeout=1)
#             assert action_when_cheap.call_count == 5

#     # @pytest.mark.skip()
#     def test_happy_path_that_schedule_on_run_continuous_calls_appropriately(self, mocker):
#         with time_machine.travel(datetime(2024, 12, 11, 0, 0, tzinfo=london_tz), tick=False) as traveller:
#             mock_price_provider = mocker.patch('requests.get')
#             mock_price_provider.return_value.status_code = 200
#             with open("./__tests__/mock_full_octopus_data.json") as f:
#                 mock_price_provider.return_value.json.return_value = json.load(f)

#             action_when_cheap = Mock()
#             action_when_expensive = Mock()

#             def run_schedule():
#                 run_octopus_agile_tariff_schedule(
#                     considered_price_count=5,
#                     action_when_cheap=action_when_cheap,
#                     action_when_expensive=action_when_expensive,
#                     run_continously=True  # Enable continuous running for the loop
#                 )

#             # schedule_thread = threading.Thread(target=run_schedule, daemon=True)
#             # schedule_thread.start()
#             run_schedule()

#             start_time = datetime.now()
#             days_to_run = 2
#             # 23 is a complete cycle, no prices for 23:00-23:59
#             end_time = start_time + timedelta(hours=24+23, minutes=30)

#             logging.debug(f"<TEST> Start time: {start_time}, End time: {end_time}")
#             while datetime.now() < end_time:
#                 traveller.shift(timedelta(minutes=15))
#                 new_mock_data_for_date = octopus_mock_data.modify_datetimes_to_be_date(
#                         date=datetime.now().isoformat().split('T')[0]
#                 )
#                 mock_price_provider.return_value.json.return_value = \
#                     new_mock_data_for_date
                
#                 logging.debug(f"<TEST> Simulated time: {datetime.now()}")
                
#                 jobs = schedule.get_jobs()

#                 if len(jobs):
#                     logging.debug(f"<TEST-R> {jobs}")
#                 time.sleep(1) # Simulates the schedule clock
            
#             # TODO added a tag to see what hour is failing, its the second schedule thats missing 2 cheap calls

#             # schedule_thread.join(timeout=1)
#             assert action_when_cheap.call_count == 5 * days_to_run
#             assert action_when_expensive.call_count == (46-15) * days_to_run