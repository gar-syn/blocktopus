import os
from datetime import timedelta
class Config(object):
    """Base configuration."""
    
    LANGUAGES = {
    'en': 'English',
    'de': 'German',
    'fr': 'French'
    }
        
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'SimpleCache'
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
        'http://0.0.0.0:8003',
        'http://localhost:8003',
    ]
    JWT_HEADER_TYPE = 'Token'


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    DB_NAME = 'blocktopus.sqlite'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    SECRET_KEY = ']g\xe9\xfc\x0e\x9a=\x1a\x96\xcd[+N]\xf1\xba2b\xf9WQ\xe3XoHZ\x86\x054\x15\xf7\xfa'
    
class DevConfig(Config):
    """Devolopment configuration."""
    ENV = 'dev'
    DEBUG = True
    TESTING = False
    DB_NAME = 'db.sqlite'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
    SECRET_KEY = '\xb7\xae\x9a\xe0>\x0c\xa1\xf6l\x12\xad#\x13\x18\x12\xc3\x89\xc6j\xce>{*\x81'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)
    
class TestConfig(Config):
    """Testing configuration."""
    
    ENV = 'test'
    TESTING = True
    DEBUG = False
    DB_NAME = 'testing.sqlite'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, 'tests', DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    SECRET_KEY = '\xbc0\xb2aM\xb3\xda\x7f\xaf\x92\x07'
    SESSION_TYPE = 'filesystem'
    WTF_CSRF_METHODS = []
    WTF_CSRF_ENABLED = False
    JWT_COOKIE_CSRF_PROTECT = False
    
configuration_classes = dict(
    dev=DevConfig,
    test=TestConfig,
    prod=ProdConfig
)