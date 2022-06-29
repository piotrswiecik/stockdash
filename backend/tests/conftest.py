"""
Pytest fixtures & setup.
Use python -m pytest -vv to avoid cross-import issues.
"""
import pytest
import os
from app import create_app


@pytest.fixture(scope='function')
def app():
    """
    Provides a Flask app instance for testing.
    :return: Flask app.
    """
    if os.environ.get('FLASK_ENV') != 'testing':
        raise Exception('Not in testing environment! Please verify FLASK_ENV setting.')

    app = create_app()

    yield app
