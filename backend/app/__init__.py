"""
This package (main) contains app factory and all relevant inits - config, logging etc.
"""
import os

from flask import Flask
from typing import Optional, Any, Mapping


def create_app(custom_config: Optional[Mapping[str, Any]] = None) -> Flask:
    """
    Main Flask app factory.
    :param custom_config: If provided as dict, overrides default config settings. Otherwise, config is loaded from
    presets, based on environment settings.
    FLASK_ENV=development for DevelopmentConfig.
    FLASK_ENV=testing for TestConfig.
    :return: Flask app instance.
    """
    app = Flask(__name__, instance_relative_config=False)  # config.py in root dir

    if not custom_config:
        app.config.from_object(''.join(['config.', os.environ.get('FLASK_ENV', 'production').title(), 'Config']))
    else:
        app.config.from_mapping(custom_config)
    print('test')
    print(app.config)

    return app

