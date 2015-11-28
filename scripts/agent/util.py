# -*- coding: UTF-8 -*-
"""util.py
"""
import sys
from ConfigParser import ConfigParser

class GetConfig(object):
    """配置读取类
    """
    def __init__(self, path):
        self.config = ConfigParser()
        self.config.read(path)

    def get_section(self, section):
        section_config = {}

        options = self.config.options(section)
        for option in options:
            try:
                section_config[option] = self.config.get(section, option)
                if section_config[option] == -1:
                    print "missing config on: %s" % option
                    sys.exit(1)
            except:
                print "exception on %s!" % option
                section_config[option] = None
                sys.exit(1)
        return section_config
