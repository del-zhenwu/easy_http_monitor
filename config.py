# -*- coding: utf-8 -*-
import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    LOG_FOLDER = os.path.join(os.environ['HOME']+'/var/easy_http/', 'logs')

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # db config
    MONGODB_HOST = '10.33.108.40'
    MONGODB_PORT = 27017
    MONGODB_NAME = 'easy_http'

    REDIS_HOST = '10.33.108.22'
    REDIS_HOST = 6379

    # ms
    MAX_REQUEST_TIMEOUT = 2000
    # s
    HTTP_SCANNER_INTERVAL = 5
    # s
    ALERTER_INTERVAL = 10
    # s
    DEFAULT_SCANNER_SECONDS = 10

    LATEST_NUM = 3

    HTTP_OK_CODE = 200
    UNKNOWN_SERVER_CODE = -100

    def __init__(self):
        pass

    @staticmethod
    def init_app():
        pass


class DevelopConfig(Config):
    DEBUG_MODE = True
    APP_PORT = 9481

    def __init__(self):
        pass


class ProdConfig(Config):
    DEBUG_MODE = False
    APP_PORT = 9482

    # db config

    def __init__(self):
        pass


def load_config():
    """加载配置类"""
    mode = os.environ.get('MODE')
    try:
        if mode == 'PROD':
            return ProdConfig()
        elif mode == 'DEVELOP':
            return DevelopConfig()
        else:
            return DevelopConfig()
    except ImportError, e:
        return None
