import pytest
from unittest.mock import Mock

import logging
from datetime import datetime
from pytest_mock import MockerFixture
import time_machine
from zoneinfo import ZoneInfo
import json
import sys
import os

from tenacity import RetryError, stop_after_attempt

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../energy_tariff_scheduler/')) 
sys.path.insert(0, module_dir)

london_tz = ZoneInfo("Europe/London")

from energy_tariff_scheduler.prices import OctopusAgilePricesClient

class TestOctopusAgilePricesClient:
    # def test_no_return_from_api(self, mocker, monkeypatch):
    #     mock_response = Mock()
    #     mock_response.status_code = 200

    #     mock_response.json.return_value = {"results": None}
    #     mocker.patch('requests.get', return_value=mock_response)

    #     client = OctopusAgilePricesClient()

    #     # ref: https://stackoverflow.com/a/67096545
    #     monkeypatch.setattr(
    #         client._request.retry, "stop", stop_after_attempt(0)
    #     )

    #     with pytest.raises(RetryError):
    #         client.get_today()

    #     mock_response.json.return_value = {"results": []}
    #     mocker.patch('requests.get', return_value=mock_response)

    #     client = OctopusAgilePricesClient()
    #     with pytest.raises(RetryError):
    #         client.get_today()

    #     mock_response.json.return_value = None
    #     mocker.patch('requests.get', return_value=mock_response)

    #     client = OctopusAgilePricesClient()
    #     with pytest.raises(RetryError):
    #         client.get_today()

    # @time_machine.travel(datetime(2023, 3, 26, 0, 24, tzinfo=london_tz))
    # def test_not_correct_length_from_api(self, mocker, monkeypatch):
    #     mock_response = Mock()
    #     mock_response.status_code = 200

    #     mock_response.json.return_value = {"results": [{"value_exc_vat": 23.4, "value_inc_vat": 24.57, "valid_from": "2023-03-26T01:00:00Z", "valid_to": "2023-03-26T01:30:00Z", "payment_method": None}]}
    #     mocker.patch('requests.get', return_value=mock_response)
    #     mocker.patch('tenacity.retry', lambda *args, **kwargs: lambda f: f)

    #     spy = mocker.spy(logging, 'warning')
        
    #     client = OctopusAgilePricesClient()
    #     monkeypatch.setattr(
    #         client._request.retry, "stop", stop_after_attempt(0)
    #     )

    #     client.get_today()

    #     assert spy.call_count == 3

    @time_machine.travel(datetime(1985, 10, 26, 0, 0, tzinfo=london_tz))
    def test_happy_path(self, mocker: MockerFixture, monkeypatch):
        mock_account_response = Mock()
        mock_account_response.status_code = 200

        mock_products_response = Mock()
        mock_products_response.status_code = 200

        mock_prices_response = Mock()
        mock_prices_response.status_code = 200

        with open("./__tests__/mock_account_response_octopus.json") as f:
            mock_account = json.load(f)
            mock_account_response.json.return_value = mock_account

        with open("./__tests__/mock_products_response_octopus.json") as f:
            mock_products = json.load(f)
            mock_products_response.json.return_value = mock_products

        with open("./__tests__/mock_prices_response_octopus.json") as f:
            mock_prices = json.load(f)
            mock_prices_response.json.return_value = mock_prices

        mock_get = mocker.patch('requests.get')

        mock_get.side_effect = [mock_account_response, mock_products_response, mock_prices_response]
    
        client = OctopusAgilePricesClient(
            api_key="mock_api_key",
            account_number="mock_account_number"
        )

        monkeypatch.setattr(
            client._request.retry, "stop", stop_after_attempt(1)
        )
        monkeypatch.setattr(
            client._get_current_tariff_and_product.retry, "stop", stop_after_attempt(1)
        )

        prices = client.get_today()

        assert len(prices) == 46

    def test_get_current_tariff_and_product(self, mocker: MockerFixture, monkeypatch):
        mock_account_response = Mock()
        mock_account_response.status_code = 200

        mock_products_response = Mock()
        mock_products_response.status_code = 200

        with open("./__tests__/mock_account_response_octopus.json") as f:
            mock_account = json.load(f)
            mock_account_response.json.return_value = mock_account

        with open("./__tests__/mock_products_response_octopus.json") as f:
            mock_products = json.load(f)
            mock_products_response.json.return_value = mock_products

        mock_get = mocker.patch('requests.get')

        mock_get.side_effect = [mock_account_response, mock_products_response]

        client = OctopusAgilePricesClient(
            api_key="mock_api_key",
            account_number="mock_account_number"
        )

        monkeypatch.setattr(
            client._get_current_tariff_and_product.retry, "stop", stop_after_attempt(1)
        )

        tariff, product = client._get_current_tariff_and_product()

        assert tariff == "E-1R-AGILE-FLEX-22-11-25-C"
        assert product == "AGILE-24-10-01" # this shows the fuzzy matching is working