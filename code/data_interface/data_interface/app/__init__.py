# -*- coding: utf-8 -*-

from celery import Celery
from flask import Flask
from config import config, Config

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app(config_name):
    """创建flask app，并用flask app的配置初始化celery
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    celery.conf.update(app.config)

    return app
