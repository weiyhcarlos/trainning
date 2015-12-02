# -*- coding: UTF-8 -*-
"""handler.py
"""

import json


#from pymongo import MongoClient

#def fail_store_local(func):
#    print("before myfunc() called.")
#    func()
#    print("  after myfunc() called.")
#    return func

class Handler(object):
    """数据处理基类
    """
    def handle_data(self, data):
        """
        根据不同处理模块使用不同的方式上报
        如：单机使用MongoDB
        """
        #TODO
        pass

class PrintMachineInfoHandler(Handler):
    """以可读形式打印机器信息数据
    """
    def handle_data(self, data):
        print json.dumps(json.loads(data), indent=4, sort_keys=True)


class MongoMachineInfoHandler(Handler):
    """使用MongoDB存储机器信息数据
    """
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.database = config['database']
        #testing
        print self.host, self.port, self.database

    def save_data(self, data):
        """完成单次记录写入
        """
        #TODO
        pass

    def handle_data(self, data):
        """将收集得到的数据组装存储到MongoDB
        """
        #TODO
        #testing
        print "upload to mongodb successfully.\n data: %s" % data

class TCPMachineInfoHandler(Handler):
    """使用TCP上报机器信息数据
    """
    def handle_data(self, data):
        #TODO
        pass
