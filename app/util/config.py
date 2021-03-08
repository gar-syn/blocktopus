import os
from datetime import timedelta

class Config(object):
    """Base configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:4100',
        'http://localhost:4100',
        'http://0.0.0.0:8000',
        'http://localhost:8000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:5000',
        'http://localhost:5000',
    ]
    JWT_HEADER_TYPE = 'Token'


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    
class DevConfig(Config):
    """Devolopment configuration."""
    
    ENV = 'dev'
    DEBUG = True
    TESTING = False
    DB_NAME = "db.sqlite"
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
    SECRET_KEY = os.urandom(24)
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)
    
class TestConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = False
    DB_NAME = 'testing.sqlite'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, 'tests', DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    SECRET_KEY = os.urandom(12)
    SESSION_TYPE = 'filesystem'
    WTF_CSRF_METHODS = []
    WTF_CSRF_ENABLED = False
    JWT_COOKIE_CSRF_PROTECT = False