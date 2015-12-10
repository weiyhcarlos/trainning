# -*- coding: UTF-8 -*-
"""收集模块
"""
from uuid import getnode as get_mac
from datetime import datetime
import socket, importlib, logging

from util import str_to_class

class Collector(object):
    """收集模块类,调用各基模块类
    属性:
        modules: 需要收集的模块string list
        module_instance: 保有模块实例
    """
    def __init__(self, modules):
        self.modules = modules
        self.module_instance = {}
        #由于要记录缓存,所以需要持有模块实例
        for module in modules:
            self.module_instance[module] = str_to_class(
                    "collector_module."+module+"_collector",
                    "".join([m.capitalize() for m in module.split("_")])
                    +"Collector")

    def set_module(self, modules):
        """更换收集模块
        参数:
            更换的模块string list
        返回:
            无
        """
        self.modules = modules
        #如果更换的模块中有未初始化的实例,实例化该模块
        for module in self.modules:
            if module not in self.module_instance.keys():
                self.module_instance[module] = str_to_class(
                    "collector_module."+module+"_collector",
                    "".join([m.capitalize() for m in module.split("_")])
                    +"Collector")

    def collect_base_info(self):
        """收集机器基础信息
        参数:
            无
        返回:
            返回机器ip,hostname,mac和time基础信息的dict
        """
        return {
            "ip":socket.gethostbyname(socket.gethostname()),
            "hostname":socket.gethostname(),
            "mac":':'.join(("%012X" % get_mac())[i:i+2]
                for i in range(0, 12, 2)),
            "time":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

    def collect_info(self):
        """收集所有基模块信息,返回字典
        参数:
            无
        返回:
            成功则返回{"status":0, "ret":收集信息dict}
            失败则返回{"status":1,"ret":error_message}
        """
        result = self.collect_base_info()
        for module in self.modules:
            instance = self.module_instance[module]
            if instance == None:
                return {
                    "status":1,
                    "ret":"class or module not found."
                }
            result[module] = instance.collect()
        return {
            "status":0,
            "ret":result
        }
