#!/usr/bin/env python
# -*- coding=utf-8 -*-


# from SocketServer import (TCPServer as TCP,
#                         StreamRequestHandler as SRH)
import socket
import logging
import json

global GLOBAL_VARS
GLOBAL_VARS = {}
BUF_SIZE = 1024


class Server(object):
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
                global GLOBAL_VARS
                sock, _ = self.tcp_sock.accept()
                read_str = sock.recv(BUF_SIZE)
                var_dict = json.loads(read_str)
                logging.info("server read:%s" % read_str)
                if "ttl" in var_dict.keys():
                    # print 'ttl in dict'
                    GLOBAL_VARS['ttl'] = var_dict['ttl']
                if "modules" in var_dict.keys():
                    ret = GLOBAL_VARS[
                        'collectObj'].set_modules(var_dict["modules"])
                    if ret['status'] == 0:
                        GLOBAL_VARS['modules'] = ret['ret']
                sock.close()
        except Exception, e:
            logging.info("error in server: %s"% e)
            exit(1)


def start_server(var):
    global GLOBAL_VARS
    GLOBAL_VARS = var
    try:
        tcp_serv = Server(GLOBAL_VARS['port'])
        tcp_serv.run()
    except Exception, e:
        logging.error(e)
        exit(0)

if __name__ == '__main__':
    start_server({'port': 10000, 'ttl': 5})
