#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from celery import Celery
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import json

import config

def make_celery(app):
    """使用celery包装flask app
    """
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL=config.CELERY_BROKER_URL,
    # CELERY_RESULT_BACKEND=config.CELERY_RESULT_BACKEND,
    INSTALLED_APPS=config.INSTALLED_APPS
)
celery = make_celery(app)

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


@app.route('/upload', methods=['POST'])
def upload():
    """接收post请求，调用后台任务处理数据
    """
    if request.data:
        try:
            data = json.loads(request.data)
        except ValueError:
            return jsonify({"ret":"invalid json data"}), 400
        try:
            if data["modules"] and data["data"]:
                upload_to_mongodb.delay(data["modules"], data["data"])
                return jsonify({"ret":""}), 200
        except KeyError:
            return jsonify({"ret":"incomplete json data"}), 400

    return jsonify({"ret":"empty json data"}), 400

if __name__ == '__main__':
    app.run(host=config.APP_HOST, port=config.APP_PORT,
            debug=config.DEBUG)
