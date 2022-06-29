"""
Environment-dependent config settings.
"""
import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(128)
    JWT_SECRET_KEY = os.urandom(128)
    LOGLEVEL = 'critical'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    LOGLEVEL = 'warning'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
                                             'postgresql+psycopg2://postgres:postgres@localhost/stockdash_dev')
    LOGLEVEL = 'debug'


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL',
                                             'postgresql+psycopg2://postgres:postgres@localhost/stockdash_test')
    LOGLEVEL = 'debug'

