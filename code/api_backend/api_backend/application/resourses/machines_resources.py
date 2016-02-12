#-*- coding: UTF-8 -*-

import time

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

class MachinesList(Resource):
    """机器列表资源
    """
    def get(self):
        ret_info = loads(MachineModel.get_machine())
        for ret in ret_info:
            ret["mac"] = ret.pop("_id")
            ret["url"] = url_for("machines_info", machine_id=ret["mac"])
        return ret_info, 200

class MachinesInfo(Resource):
    """机器信息(最新)资源
    """
    def get(self, machine_id):
        ret_info = loads(MachineModel.get_machine(machine_id))
        if not ret_info:
            return {
                "message":"invalid machine id"
            }, 400
        ret_info["mac"] = ret_info.pop("_id")
        ret_info["cpu"] = loads(CpuModel.get_cpu(ret_info["mac"]))
        ret_info["average_load"] = loads(
            AverageLoadModel.get_average_load(ret_info["mac"]))
        ret_info["memory"] = loads(
            MemoryModel.get_memory(ret_info["mac"]))
        ret_info["disk"] = loads(DiskModel.get_disk(ret_info["mac"]))
        ret_info["net"] = loads(NetModel.get_net(ret_info["mac"]))

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

    def get(self, machine_id):
        args = self.reqparse.parse_args()
        if not loads(MachineModel.get_machine(machine_id)):
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
        module = args["module"]

        module_info = {
            "cpu":CpuModel.get_cpu,
            "average_load":AverageLoadModel.get_average_load,
            "memory": MemoryModel.get_memory,
            "net": NetModel.get_net,
            "disk": DiskModel.get_disk
        }.get(module)(machine_id, begin_date, end_date)

        if module_info:
            return loads(module_info), 200
        else:
            return {
                "message":"invalid module args"
            }, 400
