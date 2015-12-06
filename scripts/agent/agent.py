# -*- coding: UTF-8 -*-
"""agent.py
"""

import argparse
import time

from collector import MachineInfoCollector
from handler import MongoMachineInfoHandler, PrintMachineInfoHandler
from parser import Parser
from util import GetConfig

CONFIG_PATH = "config.ini"

def get_option_parser():
    """返回选项解析器
    """
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False,
            prog='python agent.py',
            usage='%(prog)s [options]',
            epilog="Modules:\n  all, cpu, average_load, memory, disk, net\n"
            )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-v", "--version",
            help="show program version number and exit",
            action="store_true")
    group.add_argument("-h", "--help",
            help="show this help message and exit",
            action="store_true")
    group.add_argument("-m", "--module",
            metavar="MODULE",
            help="use module MODULE",
            choices=['all', 'cpu', 'average_load', 'mem', 'disk', 'net'],
            #nargs="+"
            )
    parser.add_argument("-t", "--ttl",
            help="set agent period, default is 60s",
            default=10)

    return parser

def main():
    """
    根据选项内容执行相应操作
    如果设置模块则读取配置内容进行监控
    """
    config = GetConfig(CONFIG_PATH)

    option_parser = get_option_parser()
    args = option_parser.parse_args()

    if args.version:
        print "version: ", config.get_section("Base")["version"]
    elif args.help:
        option_parser.print_help()
    else:
        if args.module == 'all':
            modules = config.get_section("Base")["modules"].split(",")
        else:
            modules = [args.module]

        handler = MongoMachineInfoHandler(config.get_section("MongoDB"))
        #handler = PrintMachineInfoHandler()
        collector = MachineInfoCollector()
        parser = Parser(collector, handler)
        while True:
            start_time = time.time()
            result = parser.parse(modules)
            if result["status"] == "error":
                print result.message
            else:
                print "success handle.\n"
            print "--- %s seconds ---" % (time.time() - start_time)
            time.sleep(args.ttl)

if __name__ == '__main__':
    main()
