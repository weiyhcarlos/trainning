# -*- coding: UTF-8 -*-
"""网络信息收集模块
"""

from datetime import datetime

import psutil

from . import BaseCollector

class NetCollector(BaseCollector):
    """网络信息收集类
    属性:
        last_net_info: 上次调用该模块的网络信息
        last_net_time: 上次调用该模块的时间
    """
    def __init__(self):
        self.last_net_info = None
        self.last_net_time = None

    def collect(self):
        """收集网络信息（返回每个网卡的信息）方法
        参数:
            无
        返回:
            网络信息dict
        """
        #如果是第一次调用该函数没有缓存上次调用的值,返回空字典
        if self.last_net_info is None:
            self.last_net_info = psutil.net_io_counters(pernic=True)
            self.last_net_time = datetime.now()
            return {}

        return_info = {"per_net_info":[]}

        current_net_info = psutil.net_io_counters(pernic=True)
        interval = (datetime.now()-self.last_net_time).seconds

        #根据上次缓存值计算相应速率,转为KB/S
        for name in current_net_info.keys():
            #过滤回环以及docker的网卡
            if name != "lo" and not name.startswith("veth"):
                return_info["per_net_info"].append({
                    "net_name":name,
                    "sent_rate":float(current_net_info[name].bytes_sent-
                        self.last_net_info[name].bytes_sent)/(interval*1024),
                    "recv_rate":float(current_net_info[name].bytes_recv-
                        self.last_net_info[name].bytes_recv)/(interval*1024),
                })

        #根据每个磁盘的速率计算总磁盘速率
        return_info["t_sent_rate"] = sum(u["sent_rate"] for u in
                return_info["per_net_info"])
        return_info["t_recv_rate"] = sum(u["recv_rate"] for u in
                return_info["per_net_info"])

        return return_info
