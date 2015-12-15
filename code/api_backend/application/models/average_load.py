#-*- coding: UTF-8 -*- 

from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime
from pymongo.errors import *

from . import db

class AverageLoadModel(object):
    """表结构:
    {
        "_id":object_id(),
        "machine_id":"00:00:00:00:00:00",#MAC
        "time":"2013-09-18 11:16:32"
        "w1_avg": 0.22, 
        "w2_avg": 0.44, 
        "w3_avg": 0.53
    }
    """

    @staticmethod
    def get_average_load(mac, begin_date=None, end_date=None):
        collection = db["average_load"]
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
