# -*- coding: UTF-8 -*-

import time
from collector import MachineInfoCollector

class Parser:
    '''
    使用handler处理collector收集的信息
    '''
    def __init__(self, collector, handler):
        self.handler = handler
        self.collector = collector

    def set_modules(self, modules):
        self.collector.set_modules(modules)

    def set_interval(self, interval):
        self.collector.set_interval(interval)

    def parse(self):
        while True:
            start_time = time.time()
            self.handler.upload(self.collector.collect_info())
            print("--- %s seconds ---" % (time.time() - start_time))
            time.sleep(self.collector.interval)
