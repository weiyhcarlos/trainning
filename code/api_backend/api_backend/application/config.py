#-*- coding: UTF-8 -*-

import os

# basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """配置基类
    """
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess guess'
    APP_HOST = '0.0.0.0'
    APP_PORT = 8888

    MONGO_HOST = "123.58.165.133"
    MONGO_PORT = 32774

    CONNECT = False
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """开发配置
    """
    MONGO_DATABASE = "machine_test"

class TestingConfig(Config):
    """测试配置
    """
    MONGO_DATABASE = "machine_test_test"

class ProductionConfig(Config):
    """生产配置
    """
    MONGO_DATABASE = "machine_test"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
