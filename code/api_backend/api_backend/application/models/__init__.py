#-*- coding: UTF-8 -*- 

from pymongo import MongoClient
from .. import config

client = MongoClient(config.MONGO_HOST, config.MONGO_PORT,
        connect=config.CONNECT)
db = client[config.MONGO_DATABASE]
