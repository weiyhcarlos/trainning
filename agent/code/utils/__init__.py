#!/usr/bin/env python
# -*- coding:utf-8 -*-

import importlib

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

class Tools(object):
    """utils base class
    """

    def run(self):
        pass


