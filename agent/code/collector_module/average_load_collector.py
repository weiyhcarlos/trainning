# -*- coding: UTF-8 -*-
"""平均负载收集模块
"""
import os

from . import BaseCollector

class AverageLoadCollector(BaseCollector):
    """平均负载收集类
    属性:
        无
    """
    def collect(self):
        """收集平均负载信息方法
        参数:
            无
        返回:
            负载信息dict
        """
        w1_avg, w2_avg, w3_avg = os.getloadavg()
        return {
            "w1_avg":w1_avg,
            "w2_avg":w2_avg,
            "w3_avg":w3_avg
        }


