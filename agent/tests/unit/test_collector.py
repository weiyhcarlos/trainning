#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: test_collector.py
'''

import pytest

import logging
import datetime
import socket
from uuid import getnode as get_mac

from code import collector
logging.basicConfig(level=logging.INFO)

modules = ["cpu", "memory", "disk", "net", "average_load"]

@pytest.fixture(scope="function")
def instance():
    """generate Collector instance for each test
    """
    instance = collector.Collector(modules)
    return instance

def test_set_modules(instance):
    """test for set_module function
    """
    new_modules = ["cpu"]
    ret = instance.set_modules(new_modules)
    assert ret["status"] == 0
    assert ret["ret"] == new_modules

def test_collect_info(instance):
    """test for collect_info function
    """
    now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ret = instance.collect_info()
    assert ret["status"] == 0

    for module in modules:
        assert ret["ret"][module] != None

    assert ret["ret"]["ip"] == socket.gethostbyname(socket.gethostname())
    assert ret["ret"]["hostname"] == socket.gethostname()
    assert ret["ret"]["mac"] == ':'.join(("%012X" % get_mac())[i:i+2]
            for i in range(0, 12, 2))
    assert ret["ret"]["time"] == now_date
