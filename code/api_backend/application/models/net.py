#-*- coding: UTF-8 -*- 

from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime
from pymongo.errors import *

from . import db

class NetModel(object):
    """表结构:
    {
        "_id":object_id(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32"
        "per_net_info":[
            {
                "net_name":"eth0",
                "sent_rate":100,
                "recv_rate":100,
                "packets_sent_rate":100,
                "packets_recv_rate":100,
            },
            {
                ...
            }
            ...
        ]
    }
    """
    @staticmethod
    def get_net(mac, begin_date=None, end_date=None):
        collection = db["net"]
        if not begin_date or not end_date:
            return dumps(collection.find({"machine_id": mac},
                {'_id': False}).sort( [[ "time", -1 ]] ).limit(1)[0])
        return dumps(collection.find({
                "time": {
                    "$gte": begin_date,
                    "$lte": end_date    
                },
                "machine_id":mac
            }, {'_id': False}))