import os
from pathlib import Path

from .domain import SQLALCHEMY_DATABASE_URI, LOG_LEVEL, SERVICE_PREFIX
from dotenv import load_dotenv

PROJECT_ROOT = str(Path(__file__).parent.parent)
load_dotenv()


class Config(object):
    LOG_LEVEL = os.environ.get(LOG_LEVEL, 'INFO')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    CSRF_ENABLED = True,
    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:4100',
        'http://localhost:4100',
        'http://0.0.0.0:8000',
        'http://localhost:8000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:4000',
        'http://localhost:4000',
    ]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(SQLALCHEMY_DATABASE_URI)
    SERVICE_PREFIX = os.environ.get(SERVICE_PREFIX, '')

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]