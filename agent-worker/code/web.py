#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

from flask import request

from code.app import create_app
from conf.config import config
from code.app.upload_task import upload_to_mongodb

config = config[os.getenv('FLASK_CONFIG') or 'default']

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route('/upload', methods=['POST'])
def upload():
    """接收post请求，调用后台任务处理数据
    """
    if request.data:
        try:
            data = json.loads(request.data)
        except ValueError:
            return "invalid json data", 400
        try:
            if data["modules"] and data["data"]:
                upload_to_mongodb.delay(data["modules"], data["data"])
                return "", 200
        except KeyError:
            return "incomplete json data", 400

    return "empty json data", 400

if __name__ == '__main__':
    app.run(host=config.APP_HOST, port=config.APP_PORT)
