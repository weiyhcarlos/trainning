from pymongo import MongoClient
from .. import config


client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
db = client[config.MONGO_DATABASE]
