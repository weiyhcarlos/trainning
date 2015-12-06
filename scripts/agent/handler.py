# -*- coding: UTF-8 -*-
"""handler.py
"""

import json


from pymongo import MongoClient
from pymongo.errors import *
#def fail_store_local(func):
#    print("before myfunc() called.")
#    func()
#    print("  after myfunc() called.")
#    return func

class Handler(object):
    """数据处理基类
    """
    def callback(self, prefix, name, *args):
        """存在prefix_name函数时进行调用
        """
        method = getattr(self, prefix+name, None)
        if callable(method):
            return method(*args)

    def handle(self, handle_part, data):
        """处理相应模块信息
        """
        return self.callback('handle_', handle_part, data)

    def handle_data(self, data, modules):
        """
        根据不同处理模块使用不同的方式上报
        如：单机使用MongoDB
        """
        pass

class PrintMachineInfoHandler(Handler):
    """以可读形式打印机器信息数据
    """
    def handle_data(self, data, modules):
        print json.dumps(data, indent=4, sort_keys=True)


class MongoMachineInfoHandler(Handler):
    """使用MongoDB存储机器信息数据
    """
    def __init__(self, config):
        self.client = MongoClient(config['host'], int(config['port']))
        self.database = self.client[config['database']]

    def handle_base_info(self, data):
        """上传机器基本信息
        """
        #如果是该机器信息已存入数据库,不处理该数据
        collection = self.database['machine']
        if not collection.find_one({"_id":data["_id"]}):
            collection.insert_one(data)

    def handle_cpu(self, data):
        """上传CPU信息
        """
        collection = self.database["cpu"]
        collection.insert_one(data)


    def handle_memory(self, data):
        """上传内存信息
        """
        collection = self.database["memory"]
        collection.insert_one(data)


    def handle_average_load(self, data):
        """上传平均负载信息
        """
        collection = self.database["average_load"]
        collection.insert_one(data)

    def handle_disk(self, data):
        """上传磁盘信息
        """
        collection = self.database["disk"]
        collection.insert_one(data)

    def handle_net(self, data):
        """上传网络信息
        """
        #第一次采集net速度时返回空dict, 省略
        if data:
            collection = self.database["net"]
            collection.insert_one(data)

    def handle_data(self, data, modules):
        """
        将收集得到的数据组装存储到MongoDB
        如果全部模块上传成功返回:{"status":"success","message":""}
        否则返回:{"status":"error", "message":相应错误信息}
        """
        if not modules:
            return {
                "status":"error",
                "message":"modules is not valid"
            }

        machine_info = {
            "_id":data["mac"],
            "ip":data["ip"],
            "hostname":data["hostname"]
        }
        try:
            self.handle("base_info", machine_info)
        except PyMongoError:
            return {
                    "status":"error",
                    "message":"upload machine base info fail: "
            }

        error_info = ""
        for module in modules:
            #第一次收集net信息时为空,跳过该模块处理
            if not data[module]:
                continue
            try:
                data[module]["time"] = data["time"]
                data[module]["machine_id"] = data["mac"]
                self.handle(module, data[module])
            except PyMongoError:
                error_info += ("upload " + module + " info fail\n")

        if error_info != "":
            return {
                "status":"error",
                "message":error_info
            }
        else:
            return {
                "status":"success",
                "message":""
            }


class TCPMachineInfoHandler(Handler):
    """使用TCP上报机器信息数据
    """
    def handle_data(self, data):
        #TODO
        pass
