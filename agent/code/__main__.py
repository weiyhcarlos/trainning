#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
import time
import threading
import signal
import logging

from code.utils.server import start_server
from code.utils.args_par import ArgsParse
from code.utils.check_instance import CheckInstance
from code.utils.syn_time import syn_time
from code.collector import Collector
from code.handler import Handler
from code.utils.config import Config


PATH = "../conf/config.ini"
GLOBAL_CONFIG = {}

def handler(signum, frame):
    global GLOBAL_CONFIG
    GLOBAL_CONFIG['isExited'] = True
    while True:
        if not GLOBAL_CONFIG['threadObj'].isAlive():
            sys.exit(0)
        time.sleep(1)

def log_init(file_path):
    logging.basicConfig(level=logging.DEBUG,
                        format=
                        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=file_path,
                        filemode='w'
        )

def infos_func(GLOBAL_CONFIG):
    col_obj = GLOBAL_CONFIG['collectObj']
    hand_obj = GLOBAL_CONFIG['handlerObj']
    cycle_time = 1
    while True:
        logging.info("********** %s time(s) **********" %
            str(cycle_time))
        start_time = time.time()
        info = col_obj.collect_info()
        # 收集失败,打印失败信息
        if info["status"] == 1:
            logging.info(info["ret"])
            time.sleep(GLOBAL_CONFIG["ttl"])
            continue
        logging.info("successfully collect info!")
        info["ret"]["cluster"] = GLOBAL_CONFIG["cluster"]
        handle_info = hand_obj.handle_data(
            GLOBAL_CONFIG["modules"], info["ret"])
        # 处理失败,打印错误信息
        if handle_info["status"] == 1:
            logging.info(handle_info["ret"])
        else:
            logging.info("successfully handle data!")
        interval = time.time() - start_time
        logging.info("--- %s seconds ---\n" % (interval))
        logging.info(GLOBAL_CONFIG["ttl"])
        logging.info(GLOBAL_CONFIG["modules"])
        if GLOBAL_CONFIG["ttl"] > interval:
            time.sleep(GLOBAL_CONFIG["ttl"] - interval)
        cycle_time += 1
        if GLOBAL_CONFIG["isExited"]:
            break

def main():
    """主方法
    """
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    path = "%s/%s" % (sys.path[0], PATH)
    # print path
    config = Config(path)
    result = config.run()
    if result["status"] == 1:
        return

    global GLOBAL_CONFIG
    GLOBAL_CONFIG = result["ret"].copy()
    GLOBAL_CONFIG["isExited"] = False
    is_existed = CheckInstance(GLOBAL_CONFIG["port"]).run()
    paser = ArgsParse({"isExisted": is_existed['status'],
                       "port": GLOBAL_CONFIG["port"],
                       "version": GLOBAL_CONFIG["version"]
                })
    paras = paser.run()
    # print paras
    if "modules" in paras.keys():
        GLOBAL_CONFIG["modules"] = paras["modules"]
    if "ttl" in paras.keys():
        GLOBAL_CONFIG["ttl"] = paras['ttl']
    col_obj = Collector(GLOBAL_CONFIG["modules"])
    hand_obj = Handler(GLOBAL_CONFIG["Handler"]["method"],
                       GLOBAL_CONFIG["Handler"]["config"])
    GLOBAL_CONFIG["collectObj"] = col_obj
    GLOBAL_CONFIG['handlerObj'] = hand_obj
    log_init(GLOBAL_CONFIG["logPath"])  # log file
    syn_time()  # check if ntpdate server install or not
    infos_thread = threading.Thread(target=infos_func,
                                    args=(GLOBAL_CONFIG,))
    GLOBAL_CONFIG['threadObj'] = infos_thread
    infos_thread.start()
    start_server(GLOBAL_CONFIG)

if __name__ == "__main__":
    main()
