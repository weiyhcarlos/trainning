#!/usr/bin/env python
import subprocess
import os


def syn_time():
    path = "%s/utils/syn_time.sh" % os.path.curdir
    #print path
    result = subprocess.call(["sh", path])
    return result

if __name__ == '__main__':
    syn_time()
