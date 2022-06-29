"""
This package (main) contains app factory and all relevant inits - config, logging etc.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
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

    # config handling
    if not custom_config:
        app.config.from_object(''.join(['config.', os.environ.get('FLASK_ENV', 'production').title(), 'Config']))
    else:
        app.config.from_mapping(custom_config)

    # setup & activate custom logging
    log_handler = RotatingFileHandler(
        os.path.join('instance', 'logs', ''.join(['sd_', os.environ.get('FLASK_ENV', 'undefined'), '.log'])),
        maxBytes=2**14,
        backupCount=5
    )
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')
    log_handler.setFormatter(log_formatter)
    match app.config['LOGLEVEL']:
        case 'critical':
            log_handler.setLevel(logging.CRITICAL)
        case 'error':
            log_handler.setLevel(logging.ERROR)
        case 'warning':
            log_handler.setLevel(logging.WARNING)
        case 'debug':
            log_handler.setLevel(logging.DEBUG)
        case 'info':
            log_handler.setLevel(logging.INFO)
        case _:
            log_handler.setLevel(logging.CRITICAL)  # only minimum logging when environment is undefined
    app.logger.addHandler(log_handler)
    app.logger.removeHandler(default_handler)

    app.logger.warning(f'Application started with env: {os.environ.get("FLASK_ENV")}')

    return app

