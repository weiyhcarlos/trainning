# -*- coding: UTF-8 -*-
"""handler.py
"""
#from pymongo import MongoClient

class Handler(object):
    """数据处理基类
    """
    def __init__(self, config):
        #TODO
        pass

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


    def upload(self, data):
        #TODO
        #testing
        print "upload to mongodb successfully.\n data: %s" % data
        pass

