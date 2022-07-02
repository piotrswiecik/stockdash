"""
Definition of Stock Resource for REST API.
"""
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

        if stock:
            # stock already in database - check caching
            pass
        else:
            # stock not in database - query new data from AlphaVantage
            stock = Stock(ticker)
            try:
                stock.get_timeseries_data()
                stock.get_overview_data()
                print(stock)
                stock.save()
            except ValueError as value_error:
                # separately handle API overload case!
                current_app.logger.error(f'ValueError raised by /stock/{ticker} endpoint')
                print(value_error.args)

        return stock.json(), 200
