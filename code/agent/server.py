#!/usr/bin/env python
# -*- coding=utf-8 -*-


# from SocketServer import (TCPServer as TCP,
#                         StreamRequestHandler as SRH)
import socket
from sys import exit
try:
    import simplejson as json
except ImportError:
    import json

global global_vars
global_vars = {}
BUF_SIZE = 1024


class Server:
    """start server to process request
    """

    def __init__(self, port):
        self.port = port

    def run(self):
        try:
            self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_sock.bind(('', self.port))
            self.tcp_sock.listen(5)
            self.tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            while True:
                global global_vars
                sock, addr = self.tcp_sock.accept()
                str = sock.recv(BUF_SIZE)
                var_dict = json.loads(str)
                print "server read:%s" % str
                if "ttl" in var_dict.keys():
                    # print 'ttl in dict'
                    global_vars['ttl'] = var_dict['ttl']
                if "modules" in var_dict.keys():
                    ret = global_vars[
                        'collectObj'].set_modules(var_dict["modules"])
                    if ret['status'] == 0:
                        global_vars['modules'] = ret['ret']
                sock.close()
        except Exception, e:
            print "error in server:", e
            exit(1)


def start_server(vars):
    global global_vars
    global_vars = vars
    try:
        tcpServ = Server(global_vars['port'])
        tcpServ.run()
    except Exception, e:
        print e
        exit(0)

if __name__ == '__main__':
    start_server({'port': 10000, 'ttl': 5})