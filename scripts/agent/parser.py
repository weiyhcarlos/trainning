# -*- coding: UTF-8 -*-

from collector import MachineInfoCollector

class Parser:
    '''
    使用handler处理collector收集的信息
    '''
    def __init__(self, handler):
        self.handler = handler
        self.collector = []

    def add_collector(self, collector):
        self.collector.append(collector)


class MachineInfoParser(Parser):
    def __init__(self, modules, handler):
        Parser.__init__(self, handler)
        self.add_collector(MachineInfoCollector(modules))

    def parse(self):
        for collector in self.collector:
            self.handler.upload(collector.collect_info())
