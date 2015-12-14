# -*- coding: UTF-8 -*-
"""收集模块基类
"""

class BaseCollector(object):
    """模块收集类基类
    """
    def collect(self):
        """收集方法虚函数,收集类必须实现此方法
        """
        raise NotImplementedError("模块需要定义collect函数")
