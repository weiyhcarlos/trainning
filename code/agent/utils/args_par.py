#!/usr/bin/env python
# -*- coding=utf-8 -*-

from tools import Tools
import sys
import argparse
import socket
try:
    import simplejson as json
except ImportError:
    import json


class ArgsParse(Tools):
    """analysis command line parameter
    """

    def __init__(self, dic):
        """init ArgsParse obj. [-v -m -t] paras
        Args: dic: a dict contains isExisted(instance is created or not.0 existed,1 not existed),version,port(if isExisted == 0 then port must be set)
        Return:None
        """
        self.is_existed = dic["isExisted"]
        self.version = dic['version']
        if self.is_existed == 0:
            self.port = dic["port"]
        parse = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog='python agent.py',
            usage='%(prog)s [options]',
            epilog="Modules:\n  all, cpu, average_load, memory, disk, net\n"
        )
        # parse.add_argument("-h", "--help",
        # action="store_true", help="show this help message and exit")

        parse.add_argument("-v", "--version",
                           action="store_true", help="show program version number and exit")
        parse.add_argument("-m", "--modules", nargs='*', action='store',
                           help="use modules MODULES")
        parse.add_argument("-t", "--ttl", type=int,
                           action="store", help="set agent period, default is 5s")
        self.args = parse.parse_args()

    def tcpConnect(self, msg):
        """ if isExisted == 0 then connect current instance
        Args: msg: string type, send msg
        Return: {'status':0(suc) or 1(fail)}
        """
        ret = {}
        try:
            addr = ('127.0.0.1', self.port)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(1)
            client.connect(addr)
            client.send(msg)
        except Exception:
            ret['status'] = 1
        else:
            ret['status'] = 0
        finally:
            client.close()
            return ret

    def run(self):
        """analysis  parameter and execute related flow
        Args: None
        Return: if self.isExisted == 0 then exit() else return dict{"modules":dict,"ttl":int}
        """
        ret = {}
        if self.args.version:
            print "agent current version is %s" % self.version
            sys.exit(0)
        if self.args.modules is not None:
            ret["modules"] = self.args.modules
        if self.args.ttl is not None:
            ret["ttl"] = self.args.ttl
        if self.is_existed == 0 and len(ret) > 0:
            print json.dumps(ret)
            print self.tcpConnect(json.dumps(ret))
            sys.exit(0)
        else:
            return ret
