# -*- coding: UTF-8 -*-
"""collect.py
"""
from uuid import getnode as get_mac
from datetime import datetime
import os, socket

import psutil

#from util import bytes2human

class Collector(object):
    """收集模块基类
    """
    def __init__(self, modules, interval):
        self.modules = modules
        self.interval = interval

    def callback(self, prefix, name, *args):
        method = getattr(self,prefix+name,None)
        if callable(method): return method(*args)

    def set_interval(self, interval):
        self.interval = interval

    def set_modules(self, modules):
        self.modules = modules

    def collect(self, collect_part):
        return self.callback('collect_', collect_part)

    def collect_base_info(self):
        return {
            "ip":socket.gethostbyname(socket.gethostname()),
            "hostname":socket.gethostname(),
            "mac":get_mac(),
            "time":datetime.now()
            }

    def collect_info(self):
        result = self.collect_base_info()
        print self.modules
        for collect_part in self.modules:
            result[collect_part] = self.collect(collect_part)
        return result

class MachineInfoCollector(Collector):
    """机器监控信息收集模块
    """
    def __init__(self, modules, interval):
        Collector.__init__(self, modules, interval)
        self.last_net_info = None
        self.last_disk_info = None

    def collect_cpu(self):
        cpu_info = psutil.cpu_times()
        target_info = {
            "user":cpu_info.user,
            "nice":cpu_info.nice,
            "system":cpu_info.system,
            "idle":cpu_info.idle,
            "iowait":cpu_info.iowait,
            "irq":cpu_info.irq,
            "softirq":cpu_info.softirq,
            "steal":cpu_info.steal,
            "guest":cpu_info.guest,
            "guest_nice":cpu_info.guest_nice
            }
        sum_result = sum(target_info.values())
        for key, value in target_info.iteritems():
            target_info[key] = "{0:.4f}".format(value/sum_result)
        return target_info

    def collect_average_load(self):
        w1_avg, w2_avg, w3_avg = os.getloadavg()
        return {
            "w1_avg":w1_avg,
            "w2_avg":w2_avg,
            "w3_avg":w3_avg
                }

    def collect_mem(self):
        virtual_mem_info = psutil.virtual_memory()
        swap_mem_info = psutil.swap_memory()
        target_info = {
            "total":virtual_mem_info.total,
            "used":virtual_mem_info.used,
            "abs_used":virtual_mem_info.used-virtual_mem_info.buffers-
                    virtual_mem_info.cached,
            "free":virtual_mem_info.free,
            "buffers":virtual_mem_info.buffers,
            "cached":virtual_mem_info.cached,
            "active":virtual_mem_info.active,
            "inactive":virtual_mem_info.inactive,
            "swap_used":swap_mem_info.used
        }
        for key, value in target_info.iteritems():
            target_info[key] = float(value)/1024
        return target_info


    def collect_net(self):
        #TODO
        if self.last_net_info is not None:
            net_info = psutil.net_io_counters(pernic=True)
        return_info = dict()
        for interface in net_info.keys():
            return_info[interface] = dict(net_info[interface].__dict__)
        return return_info

    def collect_disk(self):
        #TODO
        usage = []
        for part in psutil.disk_partitions(all=False):
            #跳过没有磁盘的CD-ROM驱动
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            usage.append(psutil.disk_usage(part.mountpoint))
        disk_io_info = psutil.disk_io_counters()
        return {
            "total":sum(u.total for u in usage),
            "used":sum(u.used for u in usage),
            "free":sum(u.free for u in usage),
            "read_count":disk_io_info.read_count,
            "write_count":disk_io_info.write_count,
            "read_bytes":disk_io_info.read_bytes,
            "write_bytes":disk_io_info.write_bytes,
            "read_time":disk_io_info.read_time,
            "write_time":disk_io_info.write_time
            }
