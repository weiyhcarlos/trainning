#-*- coding: UTF-8 -*- 

from bson.objectid import ObjectId
from bson.json_util import dumps
from datetime import datetime
from pymongo.errors import *

from . import db

class MachineModel(object):
    """表结构:
    {
        "_id":"00:00:00:00:00:00",#MAC
        "cluster":`xxx`,
        "ip":"1.1.1.1",
        "hostname":"XXX"
    }
    """

    @staticmethod
    def get_machine(machine_id = None):
        collection = db["machine"]
        if machine_id == None:
            return dumps(collection.find({}))
        return dumps(collection.find_one({"_id":machine_id}))