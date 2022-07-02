"""
Tests for AlphaVantage interface.
Mainly proper handling of various responses and errors.
"""
import datetime
import random

import pytest

from app.db.stockmodel import Stock
from urllib import request
from urllib.error import HTTPError

from flask import abort

from tests.mock_responses import overview_response, timeseries_response


class MockSuccessTimeSeriesResponse(object):
    """
    Represents a successful HTTP response to AlphaVantage TIME_SERIES_DAILY request.
    """
    def __init__(self, url: str) -> None:
        self.status_code = 200
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    @classmethod
    def json(cls) -> dict:
        """
        Generate mock response content as specified in TIME_SERIES_DAILY API.
        :return: Dictionary containing deserialized response data.
        """
        return timeseries_response


class MockSuccessOverviewResponse(object):
    """
    Represents a successful HTTP response to AlphaVantage OVERVIEW request.
    """
    def __init__(self, url: str) -> None:
        self.status_code = 200
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    @classmethod
    def json(cls) -> dict:
        """
        Generate mock response content as specified in OVERVIEW API.
        :return: Dictionary containing deserialized response data.
        """
        return overview_response


class MockLimitExceededResponse(object):
    """
    Represents a limit exceeded response to AlphaVantage TIME_SERIES_DAILY request.
    In this case, status is 200 but response JSON contains error message.
    """
    def __init__(self, url: str) -> None:
        self.status_code = 200
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    @classmethod
    def json(cls) -> dict:
        """
        Generate mock response content containing error message.
        :return: Dictionary containing deserialized response data.
        """
        return {
            "Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 "
                    "calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a "
                    "higher API call frequency. "
        }


class MockEmptyResponse(object):
    """
    Represents an empty response to AlphaVantage TIME_SERIES_DAILY request.
    In this case, status is 200 but response JSON contains nothing.
    """
    def __init__(self, url: str) -> None:
        self.status_code = 200
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    @classmethod
    def json(cls) -> dict:
        """
        Generate mock response content containing empty body.
        :return: Dictionary containing deserialized response data.
        """
        return {}


class MockErrorResponse(object):
    """
    Represents an error response to AlphaVantage TIME_SERIES_DAILY request.
    In this case, status is 200 but response JSON contains error message.
    """
    def __init__(self, url: str) -> None:
        self.status_code = 200
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    @classmethod
    def json(cls) -> dict:
        """
        Generate mock response content containing error message body.
        :return: Dictionary containing deserialized response data.
        """
        return {
            "Error Message": "Invalid API call. Please retry or visit the documentation "
                             "(https://www.alphavantage.co/documentation/)"
                             " for TIME_SERIES_DAILY."
        }


def test_monkeypatch_get_time_series_daily_success(monkeypatch, app, client):
    """
    Given a monkeypatched version of urllib.request.urlopen() and Stock.get_timeseries_data() method.
    When HTTP response is received as OK (200).
    Then response content conforms with ORM definition && is properly saved in DB.
    """
    def mock_http_urlopen(url: str) -> MockSuccessTimeSeriesResponse:
        return MockSuccessTimeSeriesResponse(url)

    monkeypatch.setattr(request, 'urlopen', mock_http_urlopen)

    with app.app_context():
        stock = Stock('IBM')
        stock.get_timeseries_data()  # written to test database

        db_response = Stock.query.filter_by(ticker='IBM').first()

    assert db_response
    assert db_response.ticker == 'IBM'
    assert db_response.timeseries['Meta Data']['2. Symbol'] == 'IBM'
    assert db_response.timeseries['Time Series (Daily)']['2022-06-30']['4. close'] == '141.1900'


def test_monkeypatch_get_time_series_daily_api_overloaded(monkeypatch, app):
    """
    Given a monkeypatched version of urllib.request.urlopen()
    When HTTP response is received as OK (200) but API limit is exceeded.
    Then response content contains error message & app raises ValueError to be handled by caller.
    """
    def mock_http_urlopen(url: str) -> MockLimitExceededResponse:
        return MockLimitExceededResponse(url)

    monkeypatch.setattr(request, 'urlopen', mock_http_urlopen)

    with pytest.raises(ValueError) as value_error:
        with app.app_context():
            stock = Stock('IBM')
            stock.get_timeseries_data()


def test_monkeypatch_get_time_series_daily_api_empty_response(monkeypatch, app):
    """
    Given a monkeypatched version of urllib.request.urlopen()
    When HTTP response is received as OK (200) but message body is empty.
    Then app raises ValueError to be handled by caller.
    """
    def mock_http_urlopen(url: str) -> MockEmptyResponse:
        return MockEmptyResponse(url)

    monkeypatch.setattr(request, 'urlopen', mock_http_urlopen)

    with pytest.raises(ValueError) as value_error:
        with app.app_context():
            stock = Stock('IBM')
            stock.get_timeseries_data()


def test_monkeypatch_get_time_series_daily_api_generic_error(monkeypatch, app):
    """
    Given a monkeypatched version of urllib.request.urlopen()
    When API returns status 200 but with error message (generic error e.g. due to invalid ticker).
    Then app raises ValueError to be handled by caller.
    """
    def mock_http_urlopen(url: str) -> MockErrorResponse:
        return MockErrorResponse(url)

    monkeypatch.setattr(request, 'urlopen', mock_http_urlopen)

    with pytest.raises(ValueError) as value_error:
        with app.app_context():
            stock = Stock('IBM')
            stock.get_timeseries_data()


def test_monkeypatch_get_overview_success(monkeypatch, app):
    """
    Given a monkeypatched version of urllib.request.urlopen() and Stock.get_overview_data() method.
    When HTTP response is received as OK (200).
    Then response content conforms with ORM definition && is properly saved in DB.
    """
    def mock_http_urlopen(url: str) -> MockSuccessOverviewResponse:
        return MockSuccessOverviewResponse(url)

    monkeypatch.setattr(request, 'urlopen', mock_http_urlopen)

    with app.app_context():
        stock = Stock('IBM')
        stock.get_overview_data()  # written to test database

        db_response = Stock.query.filter_by(ticker='IBM').first()

    assert db_response
    assert db_response.ticker == 'IBM'
    assert db_response.name == 'International Business Machines'
    assert 'The company began in 1911' in db_response.description
    assert db_response.exchange == 'NYSE'
    assert db_response.sector == 'Technology'
    assert db_response.industry == 'Computer & Office Equipment'
    assert db_response.market_cap == 126551425000
    assert db_response.no_shares == 896320000
    assert db_response.trail_pe_ratio == 23.19
    assert db_response.fwd_pe_ratio == 14.45
    assert db_response.d_yield == 0.0469
    assert db_response.high_52w == 144.73
    assert db_response.low_52w == 111.84
    assert db_response.eps == {'eps': 'eps'}
    assert datetime.datetime.now() - db_response.last_cache_time < datetime.timedelta(seconds=5)


def test_monkeypatch_get_overview_api_overloaded(monkeypatch, app):
    """
    Given a monkeypatched version of urllib.request.urlopen()
    When HTTP response is received as OK (200) but API limit is exceeded.
    Then response content contains error message & app raises ValueError to be handled by caller.
    """
    def mock_http_urlopen(url: str) -> MockLimitExceededResponse:
        return MockLimitExceededResponse(url)

    monkeypatch.setattr(request, 'urlopen', mock_http_urlopen)

    with pytest.raises(ValueError) as value_error:
        with app.app_context():
            stock = Stock('IBM')
            stock.get_overview_data()


def test_monkeypatch_get_overview_api_empty_response(monkeypatch, app):
    """
    Given a monkeypatched version of urllib.request.urlopen()
    When HTTP response is received as OK (200) but message body is empty.
    Then app raises ValueError to be handled by caller.
    """
    def mock_http_urlopen(url: str) -> MockEmptyResponse:
        return MockEmptyResponse(url)

    monkeypatch.setattr(request, 'urlopen', mock_http_urlopen)

    with pytest.raises(ValueError) as value_error:
        with app.app_context():
            stock = Stock('IBM')
            stock.get_overview_data()


def test_monkeypatch_get_overview_api_generic_error(monkeypatch, app):
    """
    Given a monkeypatched version of urllib.request.urlopen()
    When API returns status 200 but with error message (generic error e.g. due to invalid ticker).
    Then app raises ValueError to be handled by caller.
    """
    def mock_http_urlopen(url: str) -> MockErrorResponse:
        return MockErrorResponse(url)

    monkeypatch.setattr(request, 'urlopen', mock_http_urlopen)

    with pytest.raises(ValueError) as value_error:
        with app.app_context():
            stock = Stock('IBM')
            stock.get_overview_data()
