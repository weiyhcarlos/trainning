#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: machine.py
'''

from bson.json_util import dumps

from . import client

class MachineModel(object):
    """表结构:
    {
        "_id":"00:00:00:00:00:00",#MAC
        "cluster":`xxx`,
        "ip":"1.1.1.1",
        "hostname":"default"
    }
    """
    @staticmethod
    def get_machine(dbname, machine_id=None):
        """如果提供时间段,返回时间段内的net信息
            否则返回最新信息
        """
        collection = client[dbname]["machine"]
        if machine_id is None:
            return dumps(collection.find({}))
        return dumps(collection.find_one({"_id":machine_id}))
