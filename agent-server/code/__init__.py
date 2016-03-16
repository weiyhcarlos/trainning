#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: __init__.py
'''

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import socket
import os
from flask.ext.cors import CORS

from .resourses.machines_resources import *

from conf import config

app = Flask(__name__)
API = Api(app)

CORS(app)

API.add_resource(MachinesList, "/monitor/api/machines",
                 endpoint="machines_list")
API.add_resource(MachinesInfo,
                 '/monitor/api/machines/<string:machine_id>',
                 endpoint="machines_info")
API.add_resource(MachinesSearch,
                 "/monitor/api/machines/<string:machine_id>/search",
                 endpoint="machines_search")
