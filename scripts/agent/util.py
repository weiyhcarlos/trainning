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

#将字节转为可读形式
def bytes_to_human(n):
    """示例：
     bytes_to_human(10000)
     '9.8K'
     bytes_to_human(100001221)
     '95.4M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

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
            logging.error('Class does not exist')
    except ImportError:
        logging.error('Module does not exist')
    return class_instance
