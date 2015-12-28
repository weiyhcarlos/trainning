# -*- coding: UTF-8 -*-
"""信息处理模块
"""

from util import str_to_class

class Handler(object):
    """数据处理类
    属性:
        handler_instance: 子处理模块实例(维持连接)
    """
    def __init__(self, method, config):
        """初始化处理类
        参数:
            method:方法名
            config:配置dict
        返回:
            无
        """
        self.handler_instance = str_to_class(
                    "handler_module."+method+"_handler",
                    "".join([m.capitalize() for m in method.split("_")])
                    +"Handler", config)

    def set_handler(self, method, config):
        """更换子处理模块
        参数:
            method:方法名,
            config:配置dict
        返回:
            如果成功设置handler,返回{"status":0,"ret":""}
            设置失败,返回{"status":1,"ret":error_message}
        """
        #如果存在实例,在更换模块前清理之前模块的连接
        if self.handler_instance != None:
            self.handler_instance.destroy_connection()
        self.handler_instance = str_to_class(
                    "handler_module."+method+"_handler",
                    "".join([m.capitalize() for m in method.split("_")])
                    +"Handler", config)
        #如果实例化失败,返回错误信息
        if self.handler_instance == None:
            return {
                "status":1,
                "ret":"fail to set handler."
            }
        return {
            "status":0,
            "ret":""
        }

    def handle_data(self, modules, data):
        """调用子模块的收集方法
        参数:
            modules:["cpu","memory","average_load","net","disk"],
            data:收集得到的机器信息
        返回:
            如果全部模块上传成功返回:{"status":0,"ret":""}
            否则返回:{"status":1, "ret":相应错误信息}
        """
        if self.handler_instance == None:
            return {
                "status":1,
                "ret":"fail to load handler module."
            }
        return self.handler_instance.handle_data(modules, data)
