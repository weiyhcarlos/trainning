#-*- coding: UTF-8 -*- 

import os
from pymongo import MongoClient
from ..config import config

config = config[os.getenv('FLASK_CONFIG') or 'default']

client = MongoClient(config.MONGO_HOST, config.MONGO_PORT,
        connect=config.CONNECT)
db = client[config.MONGO_DATABASE]
