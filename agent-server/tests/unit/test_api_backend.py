#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: test_api_backend.py
'''

import pytest

import os
import json
import datetime

from conftest import client
from conftest import MACHINE_LIST, MACHINE_URL
from conf.config import config

config = config[os.getenv('FLASK_CONFIG') or 'default']

def test_machine_list(client):
    """test for getting machine list
    """
    res_data = json.loads(client.get("monitor/api/machines").data)
    for machine in res_data:
        assert machine["mac"] in MACHINE_LIST
    assert len(res_data) == 2

def test_latest_info(client):
    """test for getting latest collected info
    """
    res_data = json.loads(client.get(MACHINE_URL).data)
    for module in ("cpu", "average_load", "memory", "disk", "net"):
        assert module in res_data
        assert res_data[module]

def test_search(client):
    """test for searching by time range
    """
    test_module = ["cpu", "average_load", "disk", "net", "memory"]

    date = datetime.datetime.now()
    date_20min = date - datetime.timedelta(minutes=20)
    date_4hour = date - datetime.timedelta(hours=4)
    date_1day = date - datetime.timedelta(days=1)

    date_string = date.strftime('%Y-%m-%d %H:%M:%S')

    machine_search = MACHINE_URL + "/search?module="

    res_data_20min = json.loads(client.get(
        machine_search+",".join(test_module)+"&begin_date="+
        date_20min.strftime('%Y-%m-%d %H:%M:%S')+
        "&end_date="+date_string).data)

    res_data_4hour = json.loads(client.get(
        machine_search+",".join(test_module)+"&begin_date="+
        date_4hour.strftime('%Y-%m-%d %H:%M:%S')+
        "&end_date="+date_string).data)

    res_data_1day = json.loads(client.get(
        machine_search+",".join(test_module)+"&begin_date="+
        date_1day.strftime('%Y-%m-%d %H:%M:%S')+
        "&end_date="+date_string).data)


    for module in test_module:
        assert module in res_data_20min
        assert module in res_data_4hour
        assert module in res_data_1day
        assert 239 <= len(res_data_20min[module]) <= 240
        assert 239 <= len(res_data_4hour[module]) <= 240
        assert 23 <= len(res_data_1day[module]) <= 24
