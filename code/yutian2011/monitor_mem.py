#!/usr/bin/env python


def calc_mem():
    mems = {'result': 1}
    try:
        f = open('/proc/meminfo', 'r')
        count = 0
        for line in f.xreadlines():
            if count == 5:
                mems['result'] = 0
                break
            l = line.lower().split()
            if l[0] == 'memtotal:':
                mems['total'] = long(l[1])
                count += 1
            elif l[0] == 'memfree:':
                mems['free'] = long(l[1])
                count += 1
            elif l[0] == 'buffers:':
                mems['buffers'] = long(l[1])
                count += 1
            elif l[0] == 'cached:':
                mems['cached'] = long(l[1])
                count += 1
            elif l[0] == 'swaptotal:':
                mems['swap'] = long(l[1])
                count += 1
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        pass
    return mems


if __name__ == '__main__':
    print calc_mem()
