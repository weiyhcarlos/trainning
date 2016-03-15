#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: test_handler.py
Author:   Wei Yuhang
@contact: gzweiyuhang@corp.netease.com
@version: $Id$

Description:

Changelog:

Created: 2016-02-14 19:45
'''

import pytest

import json
import logging
from pymongo import MongoClient

import handler
logging.basicConfig(level=logging.INFO)

modules = ["cpu", "memory", "disk", "net", "average_load"]

config = {
    "http":{"uploadUrl": "http://123.58.165.132:4567/upload"},
    "mongodb": {
        "host": "123.58.165.133",
        "port": 32774,
        "database": "machine_test_dev_2",
        "localFile": "/tmp/monitor_agent.log"
    }
}

collect_info = """{"ip": "127.0.1.1", "hostname": "carloswei-PC", "average_load": {"w2_avg": 0.36, "w1_avg": 0.3,
"w3_avg": 0.31}, "cluster": "default", "mac": "3C:97:0E:0E:05:2F", "time": "2016-02-15 14:35:27", "memory":
{"abs_used": 3560849408, "active": 4110450688, "swap_used": 0, "used": 5665091584, "buffers": 329940992,
"cached": 1774301184, "inactive": 1120874496, "total": 6005563392, "free": 340471808}, "net": {"t_sent_rate":
1824.3714285714286, "t_recv_rate": 1844.8857142857144, "per_net_info": [{"sent_rate": 491.22857142857146,
"recv_rate": 223.97142857142856, "net_name": "tun0"}, {"sent_rate": 1333.142857142857, "recv_rate":
1620.9142857142858, "net_name": "wlan0"}, {"sent_rate": 0.0, "recv_rate": 0.0, "net_name": "docker0"},{"sent_rate":
0.0, "recv_rate": 0.0, "net_name": "eth0"}]}, "disk": {"t_read_rate": 351.0857142857143, "per_disk_info": [{"used":
117077708800.0, "read_rate": 0.0, "cap": 128849014784.0, "free": 11771305984.0, "write_rate": 0.0, "disk_name":
"/dev/sda7"}, {"used": 34185728000.0, "read_rate": 351.0857142857143, "cap": 52708831232.0, "free": 15821975552.0,
"write_rate": 84728.68571428572, "disk_name": "/dev/sda8"}, {"used": 63630090240.0, "read_rate": 0.0, "cap":
64426602496.0, "free": 796512256.0, "write_rate": 0.0, "disk_name": "/dev/sda1"}], "t_cap": 245984448512.0,
"t_write_rate": 84728.68571428572, "t_free": 28389793792.0, "t_used": 214893527040.0}, "cpu": {"softirq": 0.0,
"idle": 90.8, "user": 6.8, "guest_nice": 0.0, "irq": 0.0, "iowait": 0.2, "steal": 0.0, "system": 2.2, "guest": 0.0,
"nice": 0.0}}"""

@pytest.fixture(scope="function")
def http_instance():
    """generate handler instance which upload data by celery
    """
    instance = handler.Handler("http", config["http"])
    return instance

@pytest.fixture(scope="function")
def mongodb_instance():
    """generate handler instance which upload data by directly
       uploading to mongodb
    """
    instance = handler.Handler("mongodb", config["mongodb"])

    return instance
@pytest.fixture(scope="module")
def mongodb():
    """generate mongodb instance
    """
    mongo_client = MongoClient(config["mongodb"]["host"],
            config["mongodb"]["port"])
    database = mongo_client[config["mongodb"]["database"]]
    return database

def test_set_handler(http_instance):
    """test set_handler function
    """
    ret = http_instance.set_handler("mongodb", config["mongodb"])
    assert ret["status"] == 0
    assert ret["ret"] == ""

def test_http_handle_data(http_instance):
    """test for handle_data function by http, need to start
       data interface service
    """
    ret = http_instance.handle_data(modules,
            json.loads(collect_info))
    assert ret["status"] == 0

def test_mongodb_handle_data(mongodb_instance, mongodb):
    """test for handle_data function by directly uploading
    """
    ret = mongodb_instance.handle_data(modules,
            json.loads(collect_info))
    assert ret["status"] == 0
    query = {"machine_id":"3C:97:0E:0E:05:2F",
            "time":"2016-02-15 14:35:27"}
    for module in modules:
        result = mongodb[module].delete_one(query)
        assert result.deleted_count == 1

    result = mongodb["machine"].delete_one(
            {"_id":"3C:97:0E:0E:05:2F"})
    assert result.deleted_count == 1
