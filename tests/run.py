#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: run.py
Author:   Wei Yuhang
@contact: gzweiyuhang@corp.netease.com
@version: $Id$

Description:

Changelog:

Created: 2016-01-26 16:38
'''

import sys
import argparse

class ArgsParser(object):
    def __init__(self, version):
        self.version = version
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False,
            prog='python agent.py',
            usage='%(prog)s [options]',
            epilog="Modules:\n  all, agent, server, worker, api\n"
            )

        group = self.parser.add_mutually_exclusive_group(required=True)
 
        group.add_argument("-v", "--version",
             help="show program version number and exit",
             action="store_true")
        group.add_argument("-h", "--help",
             help="show this help message and exit",
             action="store_true")
        group.add_argument("-m", "--module",
              metavar="MODULE",
              help="test module MODULE",
              choices=['all', 'agent', 'server', 'wroker', 'api'],
              #nargs="+"
              )
        self.args = self.parser.parse_args()

    def run(self):
        ret = {}
        if self.args.version:
            print "run.py current version is %s" % self.version
            sys.exit(0)
        elif self.args.help:
            self.parser.print_help()
        if self.args.module is not None:
            ret["modules"] = self.args.module
        return ret

def main():
    parser = ArgsParser(version="1.0")
    params = parser.run()
 

if __name__ == "__main__":
    main()
