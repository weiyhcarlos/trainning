# -*- coding: UTF-8 -*-
"""util.py
"""
import sys, importlib
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

def str_to_class(module_name, class_name, *args):
    """动态实例化模块
    参数:
        module_name: 模块名字
        class_name: 模块类名字
    返回:
        类实例或None
    """
    class_instance = None
    try:
        module = importlib.import_module(module_name)
        try:
            class_instance = getattr(module, class_name)(*args)
        except AttributeError:
            pass
    except ImportError:
        pass
    return class_instance
