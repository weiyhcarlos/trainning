# -*- coding: UTF-8 -*-
"""handler.py
"""
#from pymongo import MongoClient

#def fail_store_local(func):
#    print("before myfunc() called.")
#    func()
#    print("  after myfunc() called.")
#    return func

class Handler(object):
    """数据处理基类
    """
    def upload(self, data):
        """
        根据不同处理模块使用不同的方式上报
        如：单机使用MongoDB
        """
        #TODO
        pass

class MongoMachineInfoHandler(Handler):
    """机器信息数据处理模块
    """
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.database = config['database']
        self.collection = config['collection']
        #testing
        print self.host, self.port, self.database, self.collection

    def save_data(self, data):
        """完成单次记录写入
        """
        #TODO
        pass

    def upload(self, data):
        """将收集得到的数据组装存储到MongoDB
        """
        #TODO
        #testing
        print "upload to mongodb successfully.\n data: %s" % data

