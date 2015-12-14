#!/usr/bin/env python
# -*- coding=utf-8 -*-
from tools import Tools
import socket
import subprocess
import string


class CheckInstance(Tools):
    """check if agent instance existed
    """

    def __init__(self, port):
        """ init CheckInstance obj
        Args: port: try to connect 127.0.0.1:port
        Return: None
        """
        self.port = port

    def run(self):
        """connect to 127.0.0.1:port
        Args: None
        Return: dict{'status':0(existed) or 1(not existed)}
        """
        ret = {}
        try:
            child = subprocess.Popen("ps -ef | grep agent.py|wc -l")
            child.wait()
            num = string.atoi(child.stdout.read())
            if num > 2:
                ret['status'] = 0
                return ret
            addr = ('127.0.0.1', self.port)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(1)
            client.connect(addr)
        except socket.error:
            ret['status'] = 0
        except Exception:
            ret['status'] = 1
        else:
            ret['status'] = 1
        finally:
            client.close()
            return ret


if __name__ == '__main__':
    ins = CheckInstance(10086)
    ret = ins.run()
    print ret
