#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: test_api_backend.py
Author:   Wei Yuhang
@contact: gzweiyuhang@corp.netease.com
@version: $Id$

Description:

Changelog:

Created: 2016-02-13 23:19
'''

import pytest

import os
import json
import logging
import datetime

from code import app
from conf.config import config

config = config[os.getenv('FLASK_CONFIG') or 'default']
logging.basicConfig(level=logging.INFO)

@pytest.fixture
def client():
    """generate flask app client
    """
    app.testing = True
    client = app.test_client()
    return client

def test_machine_list(client):
    """test for getting machine list
    """
    res_data = json.loads(client.get("monitor/api/machines").data)
    # logging.info(rv.data)
    for machine in res_data:
        assert machine["mac"] in ("00:21:5E:98:09:A8", "00:21:5E:98:09:8C")
    assert len(res_data) == 2

def test_latest_info(client):
    """test for getting latest collected info
    """
    res_data = json.loads(client.get(
        "monitor/api/machines/00:21:5E:98:09:A8").data)
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

    res_data_20min = json.loads(client.get(
        "monitor/api/machines/00:21:5E:98:09:A8/search?module="+
        ",".join(test_module)+"&begin_date="+
        date_20min.strftime('%Y-%m-%d %H:%M:%S')+
        "&end_date="+date_string).data)

    res_data_4hour = json.loads(client.get(
        "monitor/api/machines/00:21:5E:98:09:A8/search?module="+
        ",".join(test_module)+"&begin_date="+
        date_4hour.strftime('%Y-%m-%d %H:%M:%S')+
        "&end_date="+date_string).data)

    res_data_1day = json.loads(client.get(
        "monitor/api/machines/00:21:5E:98:09:A8/search?module="+
        ",".join(test_module)+"&begin_date="+
        date_1day.strftime('%Y-%m-%d %H:%M:%S')+
        "&end_date="+date_string).data)


    for module in test_module:
        assert module in res_data_20min
        assert module in res_data_4hour
        assert module in res_data_1day
        assert 239 <= len(res_data_20min[module]) <= 240
        assert 239 <= len(res_data_4hour[module]) <= 240
        assert 23 <= len(res_data_1day[module]) <= 24
