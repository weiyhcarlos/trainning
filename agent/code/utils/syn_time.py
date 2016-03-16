#!/usr/bin/env python
# -*- coding=utf-8 -*-
import subprocess
import ntplib
import time

TIMES_MAX = 3

def set_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('ntp.ubuntu.com')
    except Exception:
        return False
    else:
        tx_time = response.tx_time
        date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tx_time))
        date_process = subprocess.Popen(["date -s \"%s\" " % date_str],
                                        shell=True)
        date_process.wait()

        return True

def syn_time():
    for _ in range(TIMES_MAX):
        if set_time():
            break

if __name__ == '__main__':
    syn_time()
