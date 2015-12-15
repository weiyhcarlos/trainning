#-*- coding: UTF-8 -*- 

from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime
from pymongo.errors import *

from . import db

class DiskModel(object):
    """表结构:
    {
        "_id":object_id(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32"
        "t_cap":100,
        "t_free":100,
        "t_read_rate":100,
        "t_write_rate":100,
        "per_disk_info":[
            {
                "disk_name":"sda1",
                "cap":1000,
                "free":100,
                "read_rate":1,
                "write_rate":1,
            },
            {
                ...
            }
            ...
        ]
    }
    """
    @staticmethod
    def get_disk(mac, begin_date=None, end_date=None):
        collection = db["disk"]
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