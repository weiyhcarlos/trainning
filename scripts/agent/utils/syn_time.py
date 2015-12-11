#!/usr/bin/env python
import subprocess


def syn_time():
    result = subprocess.call(["sh", "./syn_time.sh"])
    return result

if __name__ == '__main__':
    syn_time()
