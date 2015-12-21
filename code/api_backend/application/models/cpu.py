#-*- coding: UTF-8 -*-

from bson.json_util import dumps

from . import db

class CpuModel(object):
    """表结构:
    {
        "_id":objectId(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32"
        "user":0,
        "nice":0,
        "system":0,
        "idle":0,
        "iowait":0,
        "irq":0,
        "softirq":0,
        "steal":0,
        "guest":0,
        "guest_nice":0
     }
    """
    @staticmethod
    def get_cpu(mac, begin_date=None, end_date=None):
        """如果提供时间段,返回时间段内的cpu信息
            否则返回最新信息
        """
        collection = db["cpu"]
        if not begin_date or not end_date:
            return dumps(collection.find({"machine_id": mac},
                {"_id": False, "machine_id":False}).sort(
                [["time", -1]]).limit(1)[0])
        return dumps(collection.find({
                "time": {
                    "$gte": begin_date,
                    "$lte": end_date
                },
                "machine_id":mac
            }, {"_id": False, "machine_id":False}))
