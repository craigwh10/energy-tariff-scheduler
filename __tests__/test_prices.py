import pytest
from unittest.mock import Mock

import logging
from datetime import datetime, timezone
import time_machine
from zoneinfo import ZoneInfo
import json
import sys
import os

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../energy_tariff_scheduler/')) 
sys.path.insert(0, module_dir)

london_tz = ZoneInfo("Europe/London")

from energy_tariff_scheduler.prices import OctopusAgilePricesClient

class TestOctopusAgilePricesClient:
    def test_no_return_from_api(self, mocker):
        mock_response = Mock()
        mock_response.status_code = 200

        mock_response.json.return_value = {"results": None}
        mocker.patch('requests.get', return_value=mock_response)

        client = OctopusAgilePricesClient()
        with pytest.raises(Exception, match="No data returned from the Octopus API so can't generate schedule, try running this again in a few minutes."):
            client.get_today()

        mock_response.json.return_value = {"results": []}
        mocker.patch('requests.get', return_value=mock_response)

        client = OctopusAgilePricesClient()
        with pytest.raises(Exception, match="No data returned from the Octopus API so can't generate schedule, try running this again in a few minutes."):
            client.get_today()

        mock_response.json.return_value = None
        mocker.patch('requests.get', return_value=mock_response)

        client = OctopusAgilePricesClient()
        with pytest.raises(Exception, match="No data returned from the Octopus API so can't generate schedule, try running this again in a few minutes."):
            client.get_today()

    @time_machine.travel(datetime(2023, 3, 26, 0, 24, tzinfo=london_tz))
    def test_not_correct_length_from_api(self, mocker):
        mock_response = Mock()
        mock_response.status_code = 200

        mock_response.json.return_value = {"results": [{"value_exc_vat": 23.4, "value_inc_vat": 24.57, "valid_from": "2023-03-26T01:00:00Z", "valid_to": "2023-03-26T01:30:00Z", "payment_method": None}]}
        mocker.patch('requests.get', return_value=mock_response)

        spy = mocker.spy(logging, 'warning')
        
        client = OctopusAgilePricesClient()
        client.get_today()

        assert spy.call_count == 3

    @time_machine.travel(datetime(1985, 10, 26, 0, 24, tzinfo=london_tz))
    def test_happy_path(self, mocker):
        mock_response = Mock()
        mock_response.status_code = 200
        with open("./__tests__/mock_full_octopus_data.json") as f:
            mock_response.json.return_value = json.load(f)

        mocker.patch('requests.get', return_value=mock_response)

        client = OctopusAgilePricesClient()
        prices = client.get_today()

        assert len(prices) == 46