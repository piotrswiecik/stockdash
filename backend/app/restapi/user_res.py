"""
User Resources for REST API.
"""
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from app.restapi import api  # Api class instance
from app.db.usermodel import User


class UserResource(Resource):
    pass


class UserLogin(Resource):
    """
    Represents /login API endpoint.
    Responsible for generating auth tokens.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username field is mandatory')
    parser.add_argument('password', type=str, required=True, help='Password field is mandatory')

    @classmethod
    def post(cls):
        """
        Handles /login POST request.
        Request body must contain username & password.
        If credentials are correct, JWT is generated (status 200).
        If credentials are incorrect, returns 401.
        :return: 200+JWT or 401.
        """
        args = cls.parser.parse_args(strict=True)
        user = User.get_by_username(args['username'])

        if user and user.password_correct(args['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Authorization failed'}, 401

