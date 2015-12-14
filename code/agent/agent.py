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
import time

global_vars = {}  # add collect object
PATH = "config.ini"


def main():
    """主方法
    """
    path = "%s/%s" % (sys.path[0], PATH)
    # print path
    config = Config(path)
    result = config.run()
    if result["status"] == 1:
        return
    ret = result["ret"]
    global_vars["modules"] = ret["modules"]
    global_vars["Handler"] = ret["Handler"]
    global_vars["ttl"] = ret["ttl"]
    global_vars["cluster"] = ret["cluster"]
    paser = ArgsParse({"isExisted": 0, "version": '1.0'})
    paras = paser.run()
    # print paras
    if "modules" in paras.keys():
        global_vars["modules"] = paras["modules"]
    if "ttl" in paras.keys():
        global_vars["ttl"] = paras['ttl']
    #print ret["modules"], ret["Handler"], ret["ttl"]
    col_obj = Collector(global_vars["modules"])
    hand_obj = Handler(global_vars["Handler"])
    cycle_time = 1
    while True:
        print "**********", str(cycle_time) + " time(s) **********"
        start_time = time.time()
        info = col_obj.collect_info()
        #收集失败,打印失败信息
        if info["status"] == 1:
            print info["ret"]
            time.sleep(global_vars["ttl"])
            continue
        print "successfully collect info!"
        info["ret"]["cluster"] = global_vars["cluster"]
        handle_info = hand_obj.handle_data({"modules":global_vars["modules"],
            "data":info["ret"]})
        #处理失败,打印错误信息
        if handle_info["status"] == 1:
            print handle_info["ret"]
        print "successfully handle data!"
        print "--- %s seconds ---\n" % (time.time() - start_time)
        time.sleep(global_vars["ttl"])
        cycle_time += 1


if __name__ == "__main__":
    main()
