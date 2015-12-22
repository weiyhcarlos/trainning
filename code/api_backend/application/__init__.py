#-*- coding: UTF-8 -*- 

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import socket
import os
from flask.ext.cors import CORS

from .resourses.machines_resources import *

import config

app = Flask(__name__)
# app.config['BUNDLE_ERRORS'] = True
api = Api(app)
CORS(app)

#@app.route('/')
#def hello():
#    return 'Hello World! application run successfully
#         from %s' % (socket.gethostname(), )

api.add_resource(MachinesList, "/monitor/api/machines",
        endpoint="machines_list")
api.add_resource(MachinesInfo,
        '/monitor/api/machines/<string:machine_id>',
        endpoint="machines_info")
api.add_resource(MachinesSearch,
        "/monitor/api/machines/<string:machine_id>/search",
        endpoint="machines_search")
