#!/usr/bin/env python

import fakeSerial as serial


s = serial.Serial()

print "port is", s.state
s.open()
print "port is", s.state
s.close()
print "port is", s.state
s.open()
print


s.write("test1")
s.write("test2")
print "accumulated data:", s.dataIn
print


print "readable data:\n", s.dataOut

n = 5
d = s.read(n)
print "received", n, "bytes:", d

d = s.readline().strip()
print "received line:", d

print "remaining data:\n", s.dataOut
print


if s.isOpen():
    s.close()



