#!/usr/bin/env python
# -*- coding=utf-8 -*-

import time
import server
from utils.args_par import ArgsParse
from utils.check_instance import CheckInstance
from utils.syn_time import syn_time
from collector import Collector
from handler import Handler
from utils.config import Config
import os
import sys
globalVars = {}  # add collect object
Path = "config.ini"


def main():
    path = "%s/%s" % (sys.path[0], Path)
    # print path
    config = Config(path)
    result = config.run()
    if result['status'] == 1:
        return
    ret = result["ret"]
    globalVars["modules"] = ret['modules']
    globalVars["Handler"] = ret['Handler']
    globalVars["ttl"] = ret['ttl']
    # ttl = ret['ttl']
    # print ret['modules'], ret['Handler']
    colObj = Collector(globalVars["modules"])
    handObj = Handler(globalVars["Handler"])
    while True:
        infos=colObj.collect_info()
        if infos['status']==1:
            continue
        handObj.handle_data({'modules':globalVars["modules"],'data':infos['ret']})
        time.sleep(globalVars["ttl"])


if __name__ == '__main__':
    main()
