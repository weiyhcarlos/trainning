#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: test_handler.py
'''

import pytest

import json

from code import handler
from conftest import MODULES, CONFIG, COLLECT_INFO
from conftest import mongodb

@pytest.fixture(scope="function")
def http_instance():
    """generate handler instance which upload data by celery
    """
    instance = handler.Handler("http", CONFIG["http"])
    return instance

@pytest.fixture(scope="function")
def mongodb_instance():
    """generate handler instance which upload data by directly
       uploading to mongodb
    """
    instance = handler.Handler("mongodb", CONFIG["mongodb"])
    return instance

def test_set_handler(http_instance):
    """test set_handler function
    """
    ret = http_instance.set_handler("mongodb", CONFIG["mongodb"])
    assert ret["status"] == 0
    assert ret["ret"] == ""

def test_http_handle_data(http_instance):
    """test for handle_data function by http, need to start
       data interface service
    """
    ret = http_instance.handle_data(MODULES,
            json.loads(COLLECT_INFO))
    assert ret["status"] == 0

def test_mongodb_handle_data(mongodb_instance, mongodb):
    """test for handle_data function by directly uploading
    """
    ret = mongodb_instance.handle_data(MODULES,
            json.loads(COLLECT_INFO))
    assert ret["status"] == 0
    query = {"machine_id":"3C:97:0E:0E:05:2F",
            "time":"2016-02-15 14:35:27"}
    for module in MODULES:
        result = mongodb[module].delete_one(query)
        assert result.deleted_count == 1

    result = mongodb["machine"].delete_one(
            {"_id":"3C:97:0E:0E:05:2F"})
    assert result.deleted_count == 1
