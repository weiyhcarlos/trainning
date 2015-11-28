# -*- coding: UTF-8 -*-
"""collect.py
"""

class Collector(object):
    """收集模块基类
    """
    def __init__(self, collect_list):
        #TODO 线程池初始化
        self.collect_list = collect_list

    def callback(self, prefix, name, *args):
        method = getattr(self,prefix+name,None)
        if callable(method): return method(*args)

    def collect(self, collect_part):
        return self.callback('collect_', collect_part)

    def collect_base_info(self):
        #TODO
        #收集ip,mac,hostname,time
        return dict()

    def collect_info(self):
        result = self.collect_base_info()
        #testing
        print self.collect_list
        for collect_part in self.collect_list:
            #TODO
            result[collect_part] = self.collect(collect_part)
        return result

class MachineInfoCollector(Collector):
    """机器监控信息收集模块
    """
    def collect_cpu(self):
        #TODO
        return 'test'

    def collect_average_load(self):
        #TODO
        return 'test'

    def collect_mem(self):
        #TODO
        return 'test'

    def collect_net(self):
        #TODO
        return 'test'

    def collect_disk(self):
        #TODO
        return 'test'
