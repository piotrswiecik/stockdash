"""
Tests for AlphaVantage interface.
Mainly proper handling of various responses and errors.
"""
from app.db.stockmodel import Stock
from urllib import request


class MockSuccessTimeSeriesResponse(object):
    """
    Represents a successful HTTP response to AlphaVantage TIME_SERIES_DAILY request.
    """
    def __init__(self, url) -> None:
        self.status_code = 200
        self.url = url
        self.headers = {'Content-Type': 'application/json'}

    def json(self) -> dict:
        """
        Generate mock response content as specified in TIME_SERIES_DAILY API.
        :return: Dictionary containing deserialized response data.
        """
        return {
            "Meta Data": {
                "1. Information": "Daily Prices (open, high, low, close) and Volumes",
                "2. Symbol": "IBM",
                "3. Last Refreshed": "2022-06-30",
                "4. Output Size": "Compact",
                "5. Time Zone": "US/Eastern"
            },
            "Time Series (Daily)": {
                "2022-06-30": {
                    "1. open": "139.5800",
                    "2. high": "142.4600",
                    "3. low": "139.2800",
                    "4. close": "141.1900",
                    "5. volume": "4878020"
                },
                "2022-06-29": {
                    "1. open": "142.7400",
                    "2. high": "143.5213",
                    "3. low": "139.5000",
                    "4. close": "140.7100",
                    "5. volume": "4161491"
                },
            },
        }


def test_monkeypatch_get_time_series_daily_success(monkeypatch, app, client):
    """
    Given a monkeypatched version of urllib.request.urlopen()
    When HTTP response is received as OK (200).
    Then response content conforms with ORM definition && is properly saved in DB.
    Then
    :param monkeypatch: Built-in pytest fixture.
    :return:
    """
    def mock_http_urlopen(url):
        return MockSuccessTimeSeriesResponse(url)

    monkeypatch.setattr(request, 'urlopen', mock_http_urlopen)

    stock = Stock('IBM')
    stock.get_timeseries_data()  # written to test database

    db_response = Stock.query.filter_by(ticker='IBM').first()

    assert db_response
    assert db_response.ticker == 'IBM'
    assert db_response.timeseries['Meta Data']['2. Symbol'] == 'IBM'
    assert db_response.timeseries['Time Series (Daily)']['2022-06-30']['4. close'] == '141.1900'




