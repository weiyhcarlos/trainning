# -*- coding: UTF-8 -*-
"""mongodb处理模块
"""

import json, os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from . import BaseHandler

class MongodbHandler(BaseHandler):
    """使用MongoDB存储机器信息数据
    属性:
        local_file: 继承自BaseHandler,本地存放数据路径
        client: mongodb客户端实例
        database: mongodb数据库实例
    """
    def __init__(self, config):
        BaseHandler.__init__(self, config)
        self.client = MongoClient(config['host'], int(config['port']))
        self.database = self.client[config['database']]

    def check_local_data(self):
        if os.stat(self.local_file).st_size != 0:
            lines = [line.rstrip('\n') for line in open('local_data')]
            #清空本地存储文件
            open("local_data", 'w').close()
            #存储再次上传失败的数据
            new_fail_data = []
            for line in lines:
                module, data = line.split("\t")
                try:
                    self.handle(module, json.loads(data))
                except PyMongoError:
                    new_fail_data.append((module, data))
            for fail_data in new_fail_data:
                self.store_local(fail_data[0], fail_data[1])

    def destroy_connection(self):
        self.client.close()

    def handle_data(self, params):
        """上报mongodb方法
        参数:
            params: {
                "modules":["cpu","net","average_load","disk","net"],
                "data":收集的机器信息
            }
        返回:
            如果全部模块上传成功返回:{"status":0,"ret":""}
            否则返回:{"status":1, "ret":相应错误信息}
        """
        #检查有无残留本地数据
        self.check_local_data()
        modules = params["modules"]
        data = params["data"]
        if not modules:
            return {
                "status":1,
                "ret":"modules is not valid"
            }

        machine_info = {
            "_id":data["mac"],
            "ip":data["ip"],
            "hostname":data["hostname"],
            "cluster":data["cluster"]
        }
        #机器基础信息上传mongodb
        try:
            self.handle("base_info", machine_info)
        except PyMongoError:
            return {
                    "status":1,
                    "ret":"upload machine base info fail"
            }

        error_info = ""

        #所有收集模块信息上报mongodb
        for module in modules:
            #第一次收集net信息时为空,跳过该模块处理
            if not data[module]:
                continue
            try:
                data[module]["time"] = data["time"]
                data[module]["machine_id"] = data["mac"]
                self.handle(module, data[module])
            except PyMongoError:
                self.store_local(module, data[module])
                error_info += ("upload " + module + " info fail\n")

        if error_info != "":
            return {
                "status":1,
                "ret":error_info
            }
        else:
            return {
                "status":0,
                "message":""
            }

    def handle_base_info(self, data):
        #如果是该机器信息已存入数据库,不处理该数据
        collection = self.database['machine']
        if not collection.find_one({"_id":data["_id"]}):
            collection.insert_one(data)

    def handle_cpu(self, data):
        collection = self.database["cpu"]
        collection.insert_one(data)

    def handle_memory(self, data):
        collection = self.database["memory"]
        collection.insert_one(data)

    def handle_average_load(self, data):
        collection = self.database["average_load"]
        collection.insert_one(data)

    def handle_disk(self, data):
        collection = self.database["disk"]
        collection.insert_one(data)

    def handle_net(self, data):
        #第一次采集net速度时返回空dict, 省略
        if data:
            collection = self.database["net"]
            collection.insert_one(data)
