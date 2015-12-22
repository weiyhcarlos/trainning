#!/usr/bin/env python
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
        tx = response.tx_time
        date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tx))
        ps = subprocess.Popen(["date -s \"%s\" " % date_str], shell=True)
        ps.wait()
        return True


def syn_time():
    for i in range(TIMES_MAX):
        if set_time():
            break


if __name__ == '__main__':
    syn_time()
