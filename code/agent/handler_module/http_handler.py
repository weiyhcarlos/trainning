# -*- coding: UTF-8 -*-
"""http处理模块
"""
import requests, json

from . import BaseHandler

class HttpHandler(BaseHandler):
    """使用http上报机器信息数据
    属性：
        upload_url: 数据提交接口地址
    """
    def __init__(self, config):
        self.upload_url = config["uploadUrl"]

    def handle_data(self, modules, data):
        """提交数据方法
        参数:
            modules:["cpu","net","average_load","disk","net"],
            data:收集的机器信息
        返回:
            如果提交成功返回:{"status":0,"ret":""}
            如果数据不正确返回:{"status":1, "ret":相应错误信息}
        """
        post_data = {
            "modules":modules,
            "data":data
        }
        request_result = requests.post(
            self.upload_url,
            data=json.dumps(post_data),
            headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
            )
        if request_result.status_code != 200:
            return {
                "status":1,
                "ret":json.loads(request_result.text)["ret"]
            }
        else:
            return {
                "status":0,
                "ret":""
            }

