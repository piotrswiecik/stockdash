"""
Pytest fixtures & setup.
Use python -m pytest -vv to avoid cross-import issues.
"""
import pytest
import os
from app import create_app
from app.db import db
from app.db.usermodel import User


@pytest.fixture(scope='function')
def app():
    """
    Provides a Flask app instance for testing.
    :return: Flask app.
    """
    # safety check
    if os.environ.get('FLASK_ENV') != 'testing':
        raise Exception('Not in testing environment! Please verify FLASK_ENV setting.')

    app = create_app()

    # rebuild test database with mock data
    with app.app_context():
        db.create_all()
        user = User('testuser', 'testuser@gmail.com', 'password')
        db.session.add(user)
        db.session.commit()

    yield app

    # flush test database
    with app.app_context():
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """
    Provides HTTP test client.
    :return:
    """
    with app.app_context():
        with app.test_client() as client:
            yield client

