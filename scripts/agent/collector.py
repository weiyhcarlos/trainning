# -*- coding: UTF-8 -*-
"""collect.py
"""
from uuid import getnode as get_mac
from datetime import datetime
from bson import json_util
import os, socket, json

import psutil

#from util import bytes2human

class Collector(object):
    """收集模块基类
    """
    def __init__(self, modules, interval):
        self.modules = modules
        self.interval = interval

    def callback(self, prefix, name, *args):
        """存在prefix_name函数时进行调用
        """
        method = getattr(self, prefix+name, None)
        if callable(method):
            return method(*args)

    def set_modules(self, modules):
        """更新模块
        """
        self.modules = modules

    def set_interval(self, interval):
        """更新采集周期
        """
        self.interval = interval

    def collect(self, collect_part):
        """收集相应模块的信息
        """
        return self.callback('collect_', collect_part)

    def collect_base_info(self):
        """收集机器基础信息
        """
        return {
            "ip":socket.gethostbyname(socket.gethostname()),
            "hostname":socket.gethostname(),
            "mac":':'.join(("%012X" % get_mac())[i:i+2]
                for i in range(0, 12, 2)),
            "time":datetime.now()
            }

    def collect_info(self):
        """收集所有模块信息
        """
        result = self.collect_base_info()
        for collect_part in self.modules:
            result[collect_part] = self.collect(collect_part)
        return json.dumps(result, default=json_util.default)

class MachineInfoCollector(Collector):
    """机器监控信息收集模块
    """
    def __init__(self, modules, interval):
        Collector.__init__(self, modules, interval)
        self.last_net_info = None
        self.last_disk_io = None

    def collect_cpu(self):
        """收集CPU模块信息
        """
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
            target_info[key] = value/sum_result
        return target_info

    def collect_average_load(self):
        """收集平均负载信息
        """
        w1_avg, w2_avg, w3_avg = os.getloadavg()
        return {
            "w1_avg":w1_avg,
            "w2_avg":w2_avg,
            "w3_avg":w3_avg
                }

    def collect_mem(self):
        """收集内存信息
        """
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
        """收集网络接口信息（返回每个网卡的信息）
        """
        if self.last_net_info is None:
            self.last_net_info = psutil.net_io_counters(pernic=True)
            return {}

        return_info = {"per_net_info":[]}

        current_net_info = psutil.net_io_counters(pernic=True)
        for name in current_net_info.keys():
            return_info["per_net_info"].append({
                "net_name":name,
                "sent_rate":float(current_net_info[name].bytes_sent-
                    self.last_net_info[name].bytes_sent)/(self.interval*1024),
                "recv_rate":float(current_net_info[name].bytes_recv-
                    self.last_net_info[name].bytes_recv)/(self.interval*1024),
                "packets_sent_rate":float(current_net_info[name].packets_sent-
                    self.last_net_info[name].packets_sent)/self.interval,
                "packets_recv_rate":float(current_net_info[name].packets_recv-
                    self.last_net_info[name].packets_recv)/self.interval
                })

        return return_info

    def collect_disk(self):
        """收集磁盘信息（返回总磁盘信息及每个磁盘信息）
        """
        usage = dict()

        for part in psutil.disk_partitions(all=False):
            #跳过没有磁盘的CD-ROM驱动
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            usage[part.device] = psutil.disk_usage(part.mountpoint)

        return_info = {
                "t_cap":float(sum(u.total for u in
                    usage.values()))/(1024*1024*1024),
                "t_used":float(sum(u.used for u in
                    usage.values()))/(1024*1024*1024),
                "t_free":float(sum(u.free for u in
                    usage.values()))/(1024*1024*1024),
                "t_read_rate":0.0,
                "t_write_rate":0.0,
                "per_disk_info":[]
                }

        for disk_name in usage.keys():
            return_info["per_disk_info"].append({
                    "disk_name":disk_name,
                    "cap":float(usage[disk_name].total)/(1024*1024*1024),
                    "used":float(usage[disk_name].used)/(1024*1024*1024),
                    "free":float(usage[disk_name].free)/(1024*1024*1024),
                    "write_rate":0.0,
                    "read_rate":0.0
                    })

        if self.last_disk_io is None:
            self.last_disk_io = psutil.disk_io_counters(perdisk=True)
            return return_info

        current_disk_io = psutil.disk_io_counters(perdisk=True)

        for disk_name in current_disk_io.keys():
            full_disk_name = "/dev/"+disk_name
            print full_disk_name
            if full_disk_name in usage.keys():
                for single_disk in return_info["per_disk_info"]:
                    if single_disk['disk_name'] == full_disk_name:
                        target_disk_info = single_disk
                        break
                target_disk_info["read_rate"] = float(
                        current_disk_io[disk_name].read_bytes-
                        self.last_disk_io[disk_name].read_bytes)/(
                        self.interval*1024*1024)
                target_disk_info["write_rate"] = float(
                        current_disk_io[disk_name].write_bytes-
                        self.last_disk_io[disk_name].write_bytes)/(
                        self.interval*1024*1024)


        return_info["t_write_rate"] = sum(u["write_rate"] for u in
                return_info["per_disk_info"])
        return_info["t_read_rate"] = sum(u["read_rate"] for u in
                return_info["per_disk_info"])

        return return_info
