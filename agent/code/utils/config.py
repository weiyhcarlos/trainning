#!/usr/bin/env python
# -*- coding:utf-8 -*-

from . import Tools
import yaml
try:
    import simplejson as json
except ImportError:
    import json


class Config(Tools):
    """analyze confige file with yaml
    """

    def __init__(self, config_path):
        """init Config object
        Args: configPath:  string,and path of config file
        Return: None
        """
        self.path = config_path

    def run(self):
        """ analyze config file
        Args: None
        Return: None
        """
        try:
            f = open(self.path)
            data = yaml.load(f)
            f.close()
            # ret = json.dumps(data)
            # print ret
        except IOError:
            result = {"status": 1}
            return result
        result = {}
        result["status"] = 0
        result["ret"] = data
        return result
