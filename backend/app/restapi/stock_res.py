"""
Definition of Stock Resource for REST API.
"""
import datetime

from flask import current_app
from flask_restful import Resource, reqparse
from app.db.stockmodel import Stock


class StockResource(Resource):
    """
    Represents the Stock API interface.
    """
    def get(self, ticker: str):
        """
        GET /stock/<string:ticker> endpoint.
        Extracts the full stock representation in JSON format.
        :param ticker: Ticker in string format.
        :return: Response containing JSON.
        """
        stock = Stock.get_by_ticker(ticker)
        api_response = {'status': 'null'}

        if stock:
            # check for cache status - logic is implemented inside the class
            if stock.is_cached():
                current_app.logger.debug(f'Cached response for {stock.ticker}')
                print(f'Cached response for {stock.ticker}')
                api_response = stock.json()
                api_response.update(status='cached-fresh')  # pass status to client
            # todo improve caching logic - for now OK
        else:
            # stock not in database - query new data from AlphaVantage
            stock = Stock(ticker)
            try:
                stock.get_timeseries_data()
                stock.get_overview_data()
                print(stock)
                stock.save()
                current_app.logger.debug(f'Refreshed cache for {stock.ticker}')
                print(f'Refreshed cache for {stock.ticker}')
                api_response = stock.json()
                api_response.update(status='api-fresh')  # pass status to client
            except ValueError as value_error:
                # separately handle API overload case!
                if value_error.args[0] == 'API call limit exceeded':  # todo this should not be hardcoded, refactor
                    api_response = stock.json()
                    api_response.update(status='cached-stale')
                else:
                    current_app.logger.error(f'ValueError raised by /stock/{ticker} endpoint')
                    print(value_error.args)
                    # todo implement fallback scenarios here - e.g. stale data when response empty etc.

        return api_response, 200
