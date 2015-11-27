# -*- coding: UTF-8 -*-

import argparse
import ConfigParser
import time

from collector import Collector
from handler import Handler

def get_config(section):
    '''
    读取配置
    '''
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    result = {}

    options = config.options(section)
    for option in options:
        try:
            result[option] = config.get(section, option)
            if result[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            result[option] = None
    return result

def get_parser():
    '''
    得到选项解析器
    '''
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False,
            prog='python agent.py',
            usage='%(prog)s [options]',
            epilog="Modules:\n  all,cpu,memory\n"
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
            choices=['all', 'cpu', 'memory'],
            nargs="+")
    parser.add_argument("-t", "--ttl",
            help="set agent period, default is 60s",
            default=60)
    return parser

def main():
    '''
    根据选项内容执行相应操作
    读取配置内容进行监控
    '''
    parser = get_parser()
    args = parser.parse_args()
    if args.version:
        print "agent: version 1.0"
    elif args.help:
        parser.print_help()
    elif args.ttl and args.module:
        #print args.module,args.ttl
        #print get_config("Database")
        collector = Collector(args.module)
        handler = Handler(get_config("Database"))
        while True:
            result = collector.collect()
            #print result
            handler.upload_mongodb(result)
            time.sleep(args.ttl)

if __name__ == '__main__':
    main()
