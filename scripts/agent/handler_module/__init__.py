# -*- coding: UTF-8 -*-
"""处理模块基类
"""

import json

class BaseHandler(object):
    """数据处理基类
    """
    def __init__(self, config):
        try:
            self.local_file = config["local_file"]
        except KeyError:
            self.local_file = "local_data"

    def callback(self, prefix, name, *args):
        """存在prefix+name名字的函数时进行调用
        """
        method = getattr(self, prefix+name, None)
        if callable(method):
            return method(*args)

    def handle(self, handle_part, data):
        """根据handle_part处理相应模块信息
        """
        return self.callback('handle_', handle_part, data)

    def check_local_data(self):
        """
        每次处理前检查有无本地数据,有则上传并清空
        需要子类根据不同情况实现上传
        """
        raise NotImplementedError("模块需要定义check_local_data函数")

    def store_local(self, module, data):
        """处理数据失败,保存到本地
        """
        with open(self.local_file, 'a') as local_file:
            local_file.write(module+"\t")
            json.dump(data, local_file)
            local_file.write("\n")

    def destroy_connection(self):
        """在实例销毁时做连接关闭处理
        """
        raise NotImplementedError("模块需要定义destroy函数")

    def handle_data(self, params):
        """
        根据不同处理模块使用不同的方式上报
        如：使用MongoDB
        """
        raise NotImplementedError("模块需要定义handle_data函数")
