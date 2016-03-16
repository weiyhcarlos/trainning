#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: __init__.py
'''

import os
from pymongo import MongoClient
from conf.config import config

config = config[os.getenv('FLASK_CONFIG') or 'default']

client = MongoClient(config.MONGO_HOST, config.MONGO_PORT,
                     connect=config.CONNECT)
