"""
ORM for stock.
Query formats:
DES example: https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo
TS example:
"""
import datetime
import os
import json
from urllib import request, error

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import validates
from typing import Optional, Any

from . import db


class Stock(db.Model):

    __tablename__ = 'stocks'

    # API-derived fields
    id = db.Column(db.Integer, primary_key=True)
    timeseries = db.Column(db.JSON)  # full timeseries data as JSON
    ticker = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    exchange = db.Column(db.String(8))
    sector = db.Column(db.String(30))
    industry = db.Column(db.String(30))
    market_cap = db.Column(db.BIGINT)
    no_shares = db.Column(db.BIGINT)
    trail_pe_ratio = db.Column(db.Float)
    fwd_pe_ratio = db.Column(db.Float)
    d_yield = db.Column(db.Float)
    high_52w = db.Column(db.Float)
    low_52w = db.Column(db.Float)
    eps = db.Column(db.JSON)  # format: {"fiscalDateEnding": "2022-06-30", "reportedEPS": "1.5"}
    last_cache_time = db.Column(db.DateTime)  # last API update time

    # computed fields
    # placeholder

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    @validates('ticker')
    def validate_ticker(self, key, value):
        """
        Stock ticker should be 2-10 characters long - validate.
        # todo CAUTION - unhandled ValueError!
        :param key: 'ticker' - automatically provided.
        :param value: Value of 'ticker' - automatically provided.
        :return: value if validated, raise ValueError otherwise.
        """
        if len(value) < 1 or len(value) > 10:
            return ValueError('Incorrect ticker format')
        return value

    @classmethod
    def get_by_ticker(cls, ticker: str) -> Optional['Stock']:
        """
        Find a Stock instance in DB by ticker.
        :param ticker: Ticker in string format.
        :return: Stock instance or None.
        """
        return cls.query.filter_by(ticker=ticker).first()

    def save(self) -> None:
        """
        Save current object instance to DB.
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def json(self) -> dict:
        return {
            'id': self.id,
            'ticker': self.ticker,
            'name': self.name,
            'description': self.description,
            'exchange': self.exchange,
            'sector': self.sector,
            'industry': self.industry,
            'market_cap': self.market_cap,
            'no_shares': self.no_shares,
            'trail_pe_ratio': self.trail_pe_ratio,
            'fwd_pe_ratio': self.fwd_pe_ratio,
            'd_yield': self.d_yield,
            'high_52w': self.high_52w,
            'low_52w': self.low_52w,
            'eps': '',  # placeholder
            'last_cache_time': self.last_cache_time.strftime('%Y-%m-%d:%H-%M-%S'),
            'timeseries': self.timeseries
        }

    def is_cached(self) -> bool:
        """
        Verifies if data in DB cache is fresh.
        True if last_cache_time is at most yesterday 21:15 UTC (US exchange closing time + 15).
        :return: False if data is not cached.
        """
        prev_day = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).date()
        closing_datetime = datetime.datetime(prev_day.year, prev_day.month, prev_day.day, hour=21, minute=15, second=0)
        return self.last_cache_time > closing_datetime

    def get_timeseries_data(self):
        """
        Queries AlphaVantage for price data via TIME_SERIES_DAILY API call.
        Needs access to API key stored in app config - available only in app context.
        :return: todo proper return
        """
        key = current_app.config['ALPHA_VANTAGE_API_KEY']
        if key:  # otherwise - offline mode
            query_string = current_app.config['ALPHA_VANTAGE_URL_BASE'] + 'function=TIME_SERIES_DAILY'
            query_string += '&symbol=' + self.ticker
            query_string += '&apikey=' + key

            try:
                # todo remove hardcoded message to config
                overload_message = "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per " \
                                   "minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ " \
                                   "if you would like to target a higher API call frequency. "

                query_response = request.urlopen(query_string)
                query_response_unpacked = json.loads(query_response.read())

                if 'Note' in query_response_unpacked and overload_message in query_response_unpacked['Note']:
                    raise ValueError('API call limit exceeded')

                if 'Error Message' in query_response_unpacked:
                    raise ValueError('Generic API error', query_response_unpacked['Error Message'])

                if not query_response_unpacked:
                    raise ValueError('API response empty')  # todo verify with pytest monkeypatch

                self.timeseries = query_response_unpacked
                self.last_cache_time = datetime.datetime.now(datetime.timezone.utc)

                self.save()

            except ValueError as e:
                if e.args[0] == 'API response empty':
                    current_app.logger.error(f'AV API provided empty response for {self.ticker}')
                    raise e  # bubble up
                if e.args[0] == 'API call limit exceeded':
                    current_app.logger.info(f'AV API call limit exceeded')
                    raise e  # bubble up
                if e.args[0] == 'Generic API error':
                    current_app.logger.error(f'AV API returned error response for {self.ticker}')
                    raise e  # bubble up

            except SQLAlchemyError as e:
                current_app.logger.error(f'SQLAlchemyError for {self.ticker} while saving data from API response')
                raise e  # bubble up

        # todo add error handling if offline mode - currently this method exits silently

    def get_overview_data(self):
        """
        Queries AlphaVantage for company data via OVERVIEW API call.
        Needs access to API key stored in app config - available only in app context.
        :return:
        """
        key = current_app.config['ALPHA_VANTAGE_API_KEY']
        if key:
            query_string = current_app.config['ALPHA_VANTAGE_URL_BASE'] + 'function=OVERVIEW'
            query_string += '&symbol=' + self.ticker
            query_string += '&apikey=' + key

            try:
                # todo remove hardcoded message to config
                overload_message = "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per " \
                                   "minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ " \
                                   "if you would like to target a higher API call frequency. "

                query_response = request.urlopen(query_string)
                query_response_unpacked = json.loads(query_response.read())

                if 'Note' in query_response_unpacked and overload_message in query_response_unpacked['Note']:
                    raise ValueError('API call limit exceeded')

                if 'Error Message' in query_response_unpacked:
                    raise ValueError('Generic API error', query_response_unpacked['Error Message'])

                if not query_response_unpacked:
                    raise ValueError('API response empty')

                # parsing the response and populating fields

                self.name = query_response_unpacked['Name']
                self.description = query_response_unpacked['Description']
                self.exchange = query_response_unpacked['Exchange']
                self.sector = query_response_unpacked['Sector'].lower().title()
                self.industry = query_response_unpacked['Industry'].lower().title()
                self.market_cap = query_response_unpacked['MarketCapitalization']
                self.no_shares = query_response_unpacked['SharesOutstanding']
                self.trail_pe_ratio = float(query_response_unpacked['TrailingPE'])
                self.fwd_pe_ratio = float(query_response_unpacked['ForwardPE'])
                self.d_yield = float(query_response_unpacked['DividendYield'])
                self.high_52w = float(query_response_unpacked['52WeekHigh'])
                self.low_52w = float(query_response_unpacked['52WeekLow'])
                self.eps = {'eps': 'eps'}  # todo eps

                self.save()

            except ValueError as e:
                if e.args[0] == 'API response empty':
                    current_app.logger.error(f'AV API provided empty response for {self.ticker}')
                    raise e  # bubble up
                if e.args[0] == 'API call limit exceeded':
                    current_app.logger.info(f'AV API call limit exceeded')
                    raise e  # bubble up
                if e.args[0] == 'Generic API error':
                    current_app.logger.error(f'AV API returned error response for {self.ticker}')
                    raise e  # bubble up

            except SQLAlchemyError as e:
                current_app.logger.error(f'SQLAlchemyError for {self.ticker} while saving data from API response')
                raise e  # bubble up

        # todo add error handling if offline mode - currently this method exits silently



