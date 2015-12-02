# -*- coding: UTF-8 -*-

import time

class Parser(object):
    """使用handler处理collector收集的信息
    """
    def __init__(self, collector, handler):
        self.handler = handler
        self.collector = collector

    def set_modules(self, modules):
        """更新collector的模块
        """
        self.collector.set_modules(modules)

    def set_interval(self, interval):
        """更新collector的采集周期
        """
        self.collector.set_interval(interval)

    def set_handler(self, handler):
        """更新handler
        """
        self.handler = handler

    def set_collector(self, collector):
        """更新collector
        """
        self.collector = collector

    def parse(self):
        """使用handler处理collector收集的信息
        """
        self.handler.handle_data(self.collector.collect_info())

