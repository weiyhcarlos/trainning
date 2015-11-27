# -*- coding: UTF-8 -*-

class Collector:
    '''
    收集模块
    '''
    def __init__(self, collect_list):
        #TO-DO 线程池初始化
        self.collect_list=collect_list

    def collect_cpu(self):
        #TO-DO
        return

    def collect_average_load(self):
        #TO-DO
        return

    def collect_mem(self):
        #TO-DO
        return

    def collect_net(self):
        #TO-DO
        return

    def collect_disk(self):
        #TO-DO
        return

    def collect(self):
        result = dict()
        for part in self.collect_list:
            #TO-DO
            result[part]='test'
            pass
        return result
