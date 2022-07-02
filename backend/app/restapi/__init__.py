"""
This package contains all REST API resources as a separate blueprint.
"""
from flask import Blueprint, current_app, request
from flask_restful import Api

restapi = Blueprint('restapi', __name__)
api = Api(restapi)


@restapi.before_request
def log_restapi_request() -> None:
    """
    Each request received by any REST endpoint is logged with level DEBUG.
    :return: None
    """
    current_app.logger.debug(f'Received HTTP request [{request.method}] on {request.path}')


# importing resources
from app.restapi.user_res import UserLogin
from app.restapi.stock_res import StockResource

api.add_resource(UserLogin, '/login')
api.add_resource(StockResource, '/stock/<string:ticker>')

