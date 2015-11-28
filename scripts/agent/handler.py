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

    def upload_database(self, data):
        #TODO
        pass 

    def transmission(self, data):
        #TODO
        pass

class MachineInfoHandler(Handler):
    """机器信息数据处理模块
    """
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.database = config['database']
        self.collection = config['collection']
        #testing
        print self.host, self.port, self.database, self.collection


    def upload_database(self, data):
        #TODO
        #testing
        print "upload to mongodb successfully.\n data: %s" % data
        pass

