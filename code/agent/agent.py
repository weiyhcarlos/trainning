#!/usr/bin/env python
# -*- coding=utf-8 -*-


import server
from utils.args_par import ArgsParse
from utils.check_instance import CheckInstance
from utils.syn_time import syn_time
from collector import Collector
from handler import Handler
from utils.config import Config
import sys
import time
import threading
import signal
import logging

global_vars = {}  # add collect object
PATH = "config.ini"


def handler(signum, frame):
    global global_vars
    global_vars['isExited'] = True
    while True:
        if not global_vars['threadObj'].isAlive():
            sys.exit(0)
        time.sleep(1)


def log_init(file_path):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=file_path,
                        filemode='w')


def infos_func(global_vars):
    col_obj = global_vars['collectObj']
    hand_obj = global_vars['handlerObj']
    cycle_time = 1
    while True:
        logging.info("********** %s time(s) **********" % str(cycle_time))
        start_time = time.time()
        info = col_obj.collect_info()
        # 收集失败,打印失败信息
        if info["status"] == 1:
            logging.info(info["ret"])
            time.sleep(global_vars["ttl"])
            continue
        logging.info("successfully collect info!")
        info["ret"]["cluster"] = global_vars["cluster"]
        handle_info = hand_obj.handle_data({"modules": global_vars["modules"],
                                            "data": info["ret"]})
        # 处理失败,打印错误信息
        if handle_info["status"] == 1:
            logging.info(handle_info["ret"])
        logging.info("successfully handle data!")
        interval = time.time() - start_time
        logging.info("--- %s seconds ---\n" % (interval))
        logging.info(global_vars["ttl"])
        logging.info(global_vars["modules"])
        if global_vars["ttl"] > interval:
            time.sleep(global_vars["ttl"] - interval)
        cycle_time += 1
        if global_vars["isExited"]:
            break


def main():
    """主方法
    """
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    try:
        path = "%s/%s" % (sys.path[0], PATH)
        # print path
        config = Config(path)
        result = config.run()
        if result["status"] == 1:
            return
        ret = result["ret"]
        global global_vars
        global_vars["modules"] = ret["modules"]
        global_vars["Handler"] = ret["Handler"]
        global_vars["ttl"] = ret["ttl"]
        global_vars["cluster"] = ret["cluster"]
        global_vars["port"] = ret["port"]
        global_vars["isExited"] = False
        global_vars["version"] = ret["version"]
        global_vars["logPath"] = ret["logPath"]
        is_existed = CheckInstance(global_vars["port"]).run()
        paser = ArgsParse({"isExisted": is_existed['status'], "port": global_vars[
                          "port"], "version": global_vars["version"]})
        paras = paser.run()
        # print paras
        if "modules" in paras.keys():
            global_vars["modules"] = paras["modules"]
        if "ttl" in paras.keys():
            global_vars["ttl"] = paras['ttl']
        col_obj = Collector(global_vars["modules"])
        hand_obj = Handler(global_vars["Handler"])
        global_vars["collectObj"] = col_obj
        global_vars['handlerObj'] = hand_obj
        log_init(global_vars["logPath"])  # log file
        syn_time()  # check if ntpdate server install or not
        infos_thread = threading.Thread(target=infos_func, args=(global_vars,))
        global_vars['threadObj'] = infos_thread
        infos_thread.start()
        server.start_server(global_vars)

    except Exception, e:
        print e
        sys.exit(1)


if __name__ == "__main__":
    main()
