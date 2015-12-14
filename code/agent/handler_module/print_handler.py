# -*- coding: UTF-8 -*-
"""打印处理模块--测试用
"""

import json

from . import BaseHandler


class PrintHandler(BaseHandler):
    """以可读形式打印机器信息数据
    """
    def check_local_data(self):
        pass

    def destroy_connection(self):
        pass

    def handle_data(self, params):
        """打印数据
        参数:
            params: {
                "modules":["cpu","net","average_load","disk","net"],
                "data":收集的机器信息
            }
        返回:
            如果全部模块上传成功返回:{"status":0,"ret":""}
            否则返回:{"status":1, "ret":相应错误信息}
        """
        print json.dumps(params["data"], indent=4, sort_keys=True)
        return {
            "status":0,
            "ret":""
        }

