#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: machines_resources.py
'''

import os
import datetime

from flask_restful import Resource
from flask.ext.restful import reqparse
from bson.json_util import loads
from flask import url_for

from ..models.machine import MachineModel
from ..models.cpu import CpuModel
from ..models.disk import DiskModel
from ..models.net import NetModel
from ..models.memory import MemoryModel
from ..models.average_load import AverageLoadModel
from conf.config import config

config = config[os.getenv('FLASK_CONFIG') or 'default']
DEFAULT_DB = config.MONGO_DATABASE["5s"]

class MachinesList(Resource):
    """机器列表资源
    """
    def get(self):
        ret_info = loads(MachineModel.get_machine(DEFAULT_DB))
        for ret in ret_info:
            ret["mac"] = ret.pop("_id")
            ret["url"] = url_for("machines_info", machine_id=ret["mac"])
        return ret_info, 200

class MachinesInfo(Resource):
    """机器信息(最新)资源
    """
    def get(self, machine_id):
        ret_info = loads(MachineModel.get_machine(DEFAULT_DB,
                                                  machine_id))
        if not ret_info:
            return {
                "message":"invalid machine id"
            }, 400
        ret_info["mac"] = ret_info.pop("_id")
        ret_info["cpu"] = loads(CpuModel.get_cpu(DEFAULT_DB, ret_info["mac"]))
        ret_info["average_load"] = loads(
            AverageLoadModel.get_average_load(DEFAULT_DB, ret_info["mac"]))
        ret_info["memory"] = loads(
            MemoryModel.get_memory(DEFAULT_DB, ret_info["mac"]))
        ret_info["disk"] = loads(DiskModel.get_disk(DEFAULT_DB,
                                                    ret_info["mac"]))
        ret_info["net"] = loads(NetModel.get_net(DEFAULT_DB, ret_info["mac"]))

        return ret_info, 200

class MachinesSearch(Resource):
    """机器查询信息(根据时间段)资源
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('begin_date', type=str, required=True,
            help='No begin_date provided', location='args')
        self.reqparse.add_argument('end_date', type=str, required=True,
            help='No end_date provided', location='args')
        self.reqparse.add_argument('module', type=str, required=True,
            help='No module provided', location='args')

    def _get_best_step(self, begin_date, end_date):
        """根据时间间隔得出最佳步长
           时间间隔分为5秒，1分钟，1小时，最多返回240个点
        """
        steps = config.STEPS
        begin_date = datetime.datetime.strptime(begin_date,
                                                '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(end_date,
                                              '%Y-%m-%d %H:%M:%S')

        time_diff = (end_date - begin_date).total_seconds()

        last_best_step = None
        current_best_step = None

        for step_name, step_seconds in steps.iteritems():
            if time_diff <= 240*step_seconds:
                if not last_best_step:
                    last_best_step = step_name
                elif not current_best_step:
                    current_best_step = step_name
                else:
                    last_best_step, current_best_step = \
                    current_best_step, step_name

        if not last_best_step:
            last_best_step = "1h"

        return current_best_step if current_best_step else last_best_step

    def get(self, machine_id):
        args = self.reqparse.parse_args()
        if not loads(MachineModel.get_machine(DEFAULT_DB, machine_id)):
            return {
                "message":"invalid machine id"
            }, 400
        try:
            begin_date = args["begin_date"]
            end_date = args["end_date"]
        except ValueError:
            return {
                "message": "invalid time args"
            }, 400
        modules = args["module"].split(",")
        if not modules:
            return {
                "message":"invalid module args"
            }, 400
        module_info = {}

        step = self._get_best_step(begin_date, end_date)
        for module in modules:
            module_info[module] = loads({
                "cpu":CpuModel.get_cpu,
                "average_load":AverageLoadModel.get_average_load,
                "memory": MemoryModel.get_memory,
                "net": NetModel.get_net,
                "disk": DiskModel.get_disk
            }.get(module)(config.MONGO_DATABASE[step],
                          machine_id, begin_date, end_date))
        return module_info, 200
