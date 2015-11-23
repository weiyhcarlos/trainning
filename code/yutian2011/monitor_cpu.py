#!/usr/bin/env python
import time


def calc_cpu():
    cpuinfoOld = {}
    cpuinfoNew = {}
    result = {'result': 1}
    try:
        time1=time.time()
        #print time1
        fcpu = open('/proc/stat', 'r')
        cpuList = fcpu.readline().split()
        fcpu.close()
        total = 0
        for i in xrange(1, len(cpuList)):
            total += long(cpuList[i])
        cpuinfoOld['total'] = total
        cpuinfoOld['user'] = long(cpuList[1])
        cpuinfoOld['nice'] = long(cpuList[2])
        cpuinfoOld['system'] = long(cpuList[3])
        cpuinfoOld['idle'] = long(cpuList[4])
        cpuinfoOld['irq'] = long(cpuList[5])
        time.sleep(1)
        time2=time.time()
        #print time2
        fcpu = open('/proc/stat', 'r')
        cpuList = fcpu.readline().split()
        fcpu.close()
        total = 0
        for i in xrange(1,len(cpuList)):
            total += long(cpuList[i])
        cpuinfoNew['total'] = total
        cpuinfoNew['user'] = long(cpuList[1])
        cpuinfoNew['nice'] = long(cpuList[2])
        cpuinfoNew['system'] = long(cpuList[3])
        cpuinfoNew['idle'] = long(cpuList[4])
        cpuinfoNew['irq'] = long(cpuList[5])

        total = (cpuinfoNew['total'] - cpuinfoOld['total'])
        r = time2 - time1
        total *=r
        #print r
        result['user'] = round(
            (cpuinfoNew['user'] - cpuinfoOld['user'])*100 / total, 2)
        result['nice'] = round(
            (cpuinfoNew['nice'] - cpuinfoOld['nice'])*100*r / total, 2)
        result['system'] = round(
            (cpuinfoNew['system'] - cpuinfoOld['system'])*100*r / total, 2)
        result['idle'] = round(
            (cpuinfoNew['idle'] - cpuinfoOld['idle'])*100*r / total, 2)
        result['irq'] = round(
            (cpuinfoNew['irq'] - cpuinfoOld['irq'])*100*r / total, 2)
        result['result'] = 0
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception, e:
        pass
        # raise
    else:
        pass
    finally:
        return result

if __name__ == '__main__':
    while True:
        try:
            print calc_cpu()
        except Exception,e:
            print e
            break
