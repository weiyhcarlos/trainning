# -*- coding: UTF-8 -*-
#!/bin/bash

import datetime

print "\n\ntime:"
t = datetime.time(1, 2, 3)
print t
print 'hour  :', t.hour
print 'minute:', t.minute
print 'second:', t.second
print 'microsecond:', t.microsecond
print 'tzinfo:', t.tzinfo

print 'Earliest:', datetime.time.min # Earliest: 00:00:00
print 'Latest:', datetime.time.max # Latest: 23:59:59.999999

print 'Resolution:', datetime.time.resolution # Resolution: 0:00:00.000001

#microsecond不接受浮点数
for m in [ 1, 0, 0.1, 0.6 ]:
    try:
        print '%02.1f :' % m, datetime.time(0, 0, 0, microsecond=m)
    except TypeError, err:
        print 'ERROR:', err
#1.0 : 00:00:00.000001
#0.0 : 00:00:00
#0.1 : ERROR: integer argument expected, got float
#0.6 : ERROR: integer argument expected, got float

print "\n\ndate:"
today = datetime.date.today()
print today
print 'ctime:', today.ctime()
print 'tuple:', today.timetuple()
print 'ordinal:', today.toordinal()
print 'Year:', today.year
print 'Mon :', today.month
print 'Day :', today.day
#2013-02-21
#ctime: Thu Feb 21 00:00:00 2013
#tuple: time.struct_time(tm_year=2013, tm_mon=2, tm_mday=21, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=52, tm_isdst=-1)
#ordinal: 734920
#Year: 2013
#Mon : 2
#Day : 21

print 'Earliest  :', datetime.date.min
print 'Latest    :', datetime.date.max
print 'Resolution:', datetime.date.resolution
#o: 733114
#fromordinal(o): 2008-03-13
#t: 1361446545.52
#fromtimestamp(t): 2013-02-21

d1 = datetime.date(2008, 3, 12)
print 'd1:', d1

d2 = d1.replace(year=2009)
print 'd2:', d2

print "\n\ntimedelta:"
print "microseconds:", datetime.timedelta(microseconds=1)
print "milliseconds:", datetime.timedelta(milliseconds=1)
print "seconds     :", datetime.timedelta(seconds=1)
print "minutes     :", datetime.timedelta(minutes=1)
print "hours       :", datetime.timedelta(hours=1)
print "days        :", datetime.timedelta(days=1)
print "weeks       :", datetime.timedelta(weeks=1)
#microseconds: 0:00:00.000001
#milliseconds: 0:00:00.001000
#seconds     : 0:00:01
#minutes     : 0:01:00
#hours       : 1:00:00
#days        : 1 day, 0:00:00
#weeks       : 7 days, 0:00:00

print "\n\ncomparing values:"
print 'Times--------'
t1 = datetime.time(12, 55, 0)
print '\tt1:', t1
t2 = datetime.time(13, 5, 0)
print '\tt2:', t2
print '\tt1 < t2:', t1 < t2

print 'Dates--------'
d1 = datetime.date.today()
print '\td1:', d1
d2 = datetime.date.today() + datetime.timedelta(days=1)
print '\td2:', d2
print '\td1 > d2:', d1 > d2
#Times:
#        t1: 12:55:00
#        t2: 13:05:00
#        t1 < t2: True
#Dates:
#        d1: 2013-02-21
#        d2: 2013-02-22
#        d1 > d2: False

print "\n\nFormatting and Parsing:"
format = "%a %b %d %H:%M:%S %Y"

today = datetime.datetime.today()
print 'ISO     :', today

s = today.strftime(format)
print 'strftime:', s

d = datetime.datetime.strptime(s, format)
print 'strptime:', d.strftime(format)
#ISO     : 2013-02-21 06:35:45.707450
#strftime: Thu Feb 21 06:35:45 2013
#strptime: Thu Feb 21 06:35:45 2013
