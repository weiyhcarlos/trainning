# -*- coding: UTF-8 -*-
"""处理模块基类
"""

import json

class BaseHandler(object):
    """数据处理基类
    """
    def handle_data(self, modules, data):
        """
        根据不同处理模块使用不同的方式上报
        如：使用MongoDB
        """
        raise NotImplementedError("模块需要定义handle_data函数")
