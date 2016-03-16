# -*- coding: UTF-8 -*-
"""mongodb处理模块
"""

import json
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure

from . import BaseHandler

class MongodbHandler(BaseHandler):
    """使用MongoDB存储机器信息数据
    属性:
        local_file: 本地存放数据路径
        client: mongodb客户端实例
        database: mongodb数据库实例
    """
    def __init__(self, config):
        self.local_file = config["localFile"]
        self.client = MongoClient(config['host'], int(config['port']))
        self.database = self.client[config['database']]

    def store_local(self, module, data):
        """处理数据失败,保存到本地
        """
        with open(self.local_file, 'a') as local_file:
            local_file.write(module+"\t")
            json.dump(data, local_file)
            local_file.write("\n")

    def check_local_data(self):
        """
        每次处理前检查有无本地数据,有则上传并清空
        需要子类根据不同情况实现上传
        """
        if (os.path.isfile(self.local_file) and
                os.stat(self.local_file).st_size != 0):
            lines = [line.rstrip('\n') for line in open('local_data')]
            #清空本地存储文件
            open("local_data", 'w').close()
            #存储再次上传失败的数据
            new_fail_data = []
            for line in lines:
                module, data = line.split("\t")
                try:
                    self.database[module].insert_one(json.loads(data))
                except PyMongoError:
                    new_fail_data.append((module, data))
            for fail_data in new_fail_data:
                self.store_local(fail_data[0], fail_data[1])

    def destroy_connection(self):
        """在实例销毁时做连接关闭处理
        """
        self.client.close()

    def handle_data(self, modules, data):
        """上报mongodb方法
        参数:
            modules:["cpu","net","average_load","disk","net"],
            data:收集的机器信息
        返回:
            如果全部模块上传成功返回:{"status":0,"ret":""}
            否则返回:{"status":1, "ret":相应错误信息}
        """
        #判断连接是否成功
        try:
            self.database.collection_names()
        except ConnectionFailure:
            return {
                "status":1,
                "ret":"fail to connect mongodb."
            }
        #检查有无残留本地数据
        self.check_local_data()
        if not modules:
            return {
                "status":1,
                "ret":"modules is not valid."
            }

        error_info = ""
        machine_info = {
            "_id":data["mac"],
            "ip":data["ip"],
            "hostname":data["hostname"],
            "cluster":data["cluster"]
        }
        #机器基础信息上传mongodb
        try:
            collection = self.database["machine"]
            if not collection.find_one({"_id":machine_info["_id"]}):
                collection.insert_one(machine_info)
        except PyMongoError:
            self.store_local("machine", machine_info)
            error_info += ("upload machine base info fail.\n")


        #所有收集模块信息上报mongodb
        for module in modules:
            if module not in data:
                return {
                    "status":1,
                    "ret":"can not find module in data."
                }
            #第一次收集net信息时为空,跳过该模块处理
            if not data[module]:
                continue
            data[module]["time"] = data["time"]
            data[module]["machine_id"] = data["mac"]
            try:
                self.database[module].insert_one(data[module])
            except PyMongoError:
                self.store_local(module, data[module])
                error_info += ("upload " + module + " info fail.\n")

        #如果上传失败,转存数据到本地,返回失败,加上哪个模块上传失败的信息
        if error_info != "":
            return {
                "status":1,
                "ret":error_info
            }
        return {
            "status":0,
            "ret":""
        }
