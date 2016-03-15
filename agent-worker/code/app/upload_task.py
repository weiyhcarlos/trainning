# -*- coding: utf-8 -*-

import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from . import celery
from config import config

config = config[os.getenv('FLASK_CONFIG') or 'default']

client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
database = client[config.MONGO_DATABASE]

#任务异常时30秒之后进行重试
@celery.task(name="web.upload_to_mongodb", bind=True,
    default_retry_delay=30)
def upload_to_mongodb(self, modules, data):
    """celery后台任务，负责将信息上传到mongodb
    """
    machine_info = {
        "_id":data["mac"],
        "ip":data["ip"],
        "hostname":data["hostname"],
        "cluster":data["cluster"]
    }
    #机器基础信息上传mongodb
    collection = database["machine"]
    try:
        if not collection.find_one({"_id":machine_info["_id"]}):
            collection.insert_one(machine_info)
    except PyMongoError as exc:
        raise self.retry(exc=exc)

    #所有收集模块信息上报mongodb
    for module in modules:
        if module not in data:
            return
        #第一次收集net信息时为空,跳过该模块处理
        if not data[module]:
            continue
        data[module]["time"] = data["time"]
        data[module]["machine_id"] = data["mac"]
        collection = database[module]
        try:
            if not collection.find_one({"machine_id":data["mac"],
                "time":data["time"]}):
                collection.insert_one(data[module])
        except PyMongoError as exc:
            raise self.retry(exc=exc)
