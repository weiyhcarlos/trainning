#!/usr/bin/env python
# -*- encoding=utf8 -*-
"""
Filename: test_interface.py
"""

import os
import json
import pytest

from conftest import MODULES, COLLECT_INFO
from conftest import client, mongodb

def test_upload(client, mongodb):
    """test for /upload api
    """
    post_data = dict(
            modules=MODULES,
            data=json.loads(COLLECT_INFO)
        )
    res_data = client.post("/upload", data=json.dumps(post_data))
    assert res_data.status_code == 200

    query = {"machine_id":"3C:97:0E:0E:05:2F", "time":"2016-02-14 14:35:27"}
    for module in MODULES:
        result = mongodb[module].delete_one(query)
        assert result.deleted_count == 1

    result = mongodb["machine"].delete_one({"_id":"3C:97:0E:0E:05:2F"})
    assert result.deleted_count == 1
