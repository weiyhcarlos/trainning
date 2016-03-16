#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: net.py
'''

from bson.json_util import dumps

from . import client

class NetModel(object):
    """表结构:
    {
        "_id":object_id(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32",
        "t_sent_rate":100,
        "t_recv_rate":100,
        "per_net_info":[
            {
                "net_name":"eth0",
                "sent_rate":100,
                "recv_rate":100,
            },
            {
                ...
            }
            ...
        ]
    }
    """
    @staticmethod
    def get_net(dbname, mac, begin_date=None, end_date=None):
        """如果提供时间段,返回时间段内的net信息
            否则返回最新信息
        """
        collection = client[dbname]["net"]
        if not begin_date or not end_date:
            return dumps(collection.find({"machine_id": mac},
                                         {"_id": False, "machine_id":False}
                                        ).sort([["time", -1]]).limit(1)[0])
        return dumps(collection.find({
            "time": {
                "$gte": begin_date,
                "$lte": end_date
                },
            "machine_id":mac
            }, {"_id": False, "machine_id":False}))
