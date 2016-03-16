#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: conftest.py
'''

import pytest
from code import app

MACHINE_LIST = ("00:21:5E:98:09:A8", "00:21:5E:98:09:8C",)

MACHINE_URL = "monitor/api/machines/00:21:5E:98:09:A8"

@pytest.fixture
def client():
    """generate flask app client
    """
    app.testing = True
    client = app.test_client()
    return client
