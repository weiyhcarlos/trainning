# -*- coding: UTF-8 -*-
"""磁盘信息收集模块
"""

import os
from datetime import datetime

import psutil

from . import BaseCollector

class DiskCollector(BaseCollector):
    """磁盘信息收集类
    属性:
        lask_disk_io: 记录上次调用该模块的磁盘IO信息
        lask_disk_time: 记录上次调用该模块的时间
    """
    def __init__(self):
        self.last_disk_io = None
        self.last_disk_time = None

    def collect(self):
        """收集磁盘信息（返回总磁盘信息及每个磁盘信息）方法
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
                    usage.values())),
                "t_used":float(sum(u.used for u in
                    usage.values())),
                "t_free":float(sum(u.free for u in
                    usage.values())),
                "t_read_rate":0.0,
                "t_write_rate":0.0,
                "per_disk_info":[]
                }
        #获得每块磁盘的信息
        for disk_name in usage.keys():
            return_info["per_disk_info"].append({
                    "disk_name":disk_name,
                    "cap":float(usage[disk_name].total),
                    "used":float(usage[disk_name].used),
                    "free":float(usage[disk_name].free),
                    "write_rate":0.0,
                    "read_rate":0.0
                    })

        #如果是第一次调用该函数没有缓存上次调用的值,
        #不计算速率部分直接返回磁盘使用信息
        if self.last_disk_io is None:
            self.last_disk_io = psutil.disk_io_counters(perdisk=True)
            self.last_disk_time = datetime.now()
            return return_info

        current_disk_io = psutil.disk_io_counters(perdisk=True)
        interval = (datetime.now() - self.last_disk_time).seconds

        if interval == 0:
            return return_info

        #根据上次缓存值计算相应速率,转为MB/S
        for disk_name in current_disk_io.keys():
            full_disk_name = "/dev/"+disk_name
            if full_disk_name in usage.keys():
                for single_disk in return_info["per_disk_info"]:
                    if single_disk['disk_name'] == full_disk_name:
                        target_disk_info = single_disk
                        break
                target_disk_info["read_rate"] = float(
                        current_disk_io[disk_name].read_bytes-
                        self.last_disk_io[disk_name].read_bytes)/(
                        interval)
                target_disk_info["write_rate"] = float(
                        current_disk_io[disk_name].write_bytes-
                        self.last_disk_io[disk_name].write_bytes)/(
                        interval)

        #根据每个磁盘的速率计算总磁盘速率
        return_info["t_write_rate"] = sum(u["write_rate"] for u in
                return_info["per_disk_info"])
        return_info["t_read_rate"] = sum(u["read_rate"] for u in
                return_info["per_disk_info"])

        return return_info
