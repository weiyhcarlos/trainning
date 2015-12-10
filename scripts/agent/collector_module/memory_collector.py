# -*- coding: UTF-8 -*-
"""内存信息收集模块
"""

import psutil

from . import BaseCollector

class MemoryCollector(BaseCollector):
    """内存信息收集模块
    属性:
        无
    """
    def collect(self):
        """收集内存信息方法
        参数:
            无
        返回:
            内存信息dict
        """
        #内存使用情况
        virtual_mem_info = psutil.virtual_memory()
        #交换内存使用情况
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
        #将数值转为MB
        for key, value in target_info.iteritems():
            target_info[key] = float(value)/(1024*1024)
        return target_info
