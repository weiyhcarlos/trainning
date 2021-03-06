# -*- coding: UTF-8 -*-
"""cpu使用率收集模块
"""

import psutil

from . import BaseCollector

class CpuCollector(BaseCollector):
    """CPU使用率收集类
    属性:
        无
    """
    def collect(self):
        """收集CPU使用率方法
        参数:
            无
        返回:
            CPU使用率dict
        """
        cpu_info = psutil.cpu_times_percent()
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
        return target_info

