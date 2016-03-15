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

PATH = "../conf/config.ini"

def handler(signum, frame):
    global global_config
    global_config['isExited'] = True
    while True:
        if not global_config['threadObj'].isAlive():
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


def infos_func(global_config):
    col_obj = global_config['collectObj']
    hand_obj = global_config['handlerObj']
    cycle_time = 1
    while True:
        logging.info("********** %s time(s) **********" % 
            str(cycle_time))
        start_time = time.time()
        info = col_obj.collect_info()
        # 收集失败,打印失败信息
        if info["status"] == 1:
            logging.info(info["ret"])
            time.sleep(global_config["ttl"])
            continue
        logging.info("successfully collect info!")
        info["ret"]["cluster"] = global_config["cluster"]
        handle_info = hand_obj.handle_data(
            global_config["modules"], info["ret"])
        # 处理失败,打印错误信息
        if handle_info["status"] == 1:
            logging.info(handle_info["ret"])
        else:
            logging.info("successfully handle data!")
        interval = time.time() - start_time
        logging.info("--- %s seconds ---\n" % (interval))
        logging.info(global_config["ttl"])
        logging.info(global_config["modules"])
        if global_config["ttl"] > interval:
            time.sleep(global_config["ttl"] - interval)
        cycle_time += 1
        if global_config["isExited"]:
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

        global global_config
        global_config = result["ret"].copy()
        global_config["isExited"] = False

        is_existed = CheckInstance(global_config["port"]).run()
        paser = ArgsParse({"isExisted": is_existed['status'],
                "port": global_config["port"], 
                "version": global_config["version"]
                })
        paras = paser.run()
        # print paras
        if "modules" in paras.keys():
            global_config["modules"] = paras["modules"]
        if "ttl" in paras.keys():
            global_config["ttl"] = paras['ttl']
        col_obj = Collector(global_config["modules"])
        hand_obj = Handler(global_config["Handler"]["method"],
                global_config["Handler"]["config"])
        global_config["collectObj"] = col_obj
        global_config['handlerObj'] = hand_obj
        log_init(global_config["logPath"])  # log file
        syn_time()  # check if ntpdate server install or not
        infos_thread = threading.Thread(target=infos_func,
            args=(global_config,))
        global_config['threadObj'] = infos_thread
        infos_thread.start()
        server.start_server(global_config)

    except Exception, e:
        print e
        sys.exit(1)


if __name__ == "__main__":
    main()
