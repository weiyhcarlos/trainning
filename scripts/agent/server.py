#!/usr/bin/env python
# -*- coding=utf-8 -*-


from SocketServer import (TCPServer as TCP,
                          StreamRequestHandler as SRH)
#import socket
from agent import globalVars
try:
    import simplejson as json
except ImportError:
    import json


class Server(SRH):
    """start server to process request
    """

    def handle(self):
        """set global vars
        """
        try:
            global globalVars  # global vars from agent.py
            self.str = self.rfile.readline().strip()
            varDict = json.loads(self.str)
            if "ttl" in varDict.keys():
                globalVars['ttl'] = varDict['ttl']
            if "modules" in varDict.keys():
                globalVars['modules'] = globalVars['collectObj'].set()
        except ValueError:
            pass


def startServer(port):
    addr = ('', port)
    tcpServ = TCP(addr, Server)
    tcpServ.serve_forever()
