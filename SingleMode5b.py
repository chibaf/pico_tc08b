#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# TC-08 SINGLE MODE EXAMPLE


import ctypes
import numpy as np
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
import sys

from time import sleep

import time
import datetime

from pylab import *

filename = sys.argv[1];

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open unit
status["open_unit"] = tc08.usb_tc08_open_unit()
assert_pico2000_ok(status["open_unit"])
chandle = status["open_unit"]

# set mains rejection to 50 Hz
status["set_mains"] = tc08.usb_tc08_set_mains(chandle,0)
assert_pico2000_ok(status["set_mains"])

# set up channel
# therocouples types and int8 equivalent
# B=66 , E=69 , J=74 , K=75 , N=78 , R=82 , S=83 , T=84 , ' '=32 , X=88 
f=open(filename,"w+")
len=8
d = datetime.datetime.today()
start = time.time()
print("start time: ",d)
elapsed_time=0
temps=[0]*8
y=[0]*10
#while elapsed_time < 420.1:
f.write("start time: ")
f.write(str(d))
f.write("\n")
while True:
  try:
#  sleep(0.3)
    f.write(str(elapsed_time)+", "	)
    for i in range(1,len+1):
      typeK = ctypes.c_int8(75)
      status["set_channel"] = tc08.usb_tc08_set_channel(chandle, i, typeK)
      assert_pico2000_ok(status["set_channel"])

# get minimum sampling interval in ms
      status["get_minimum_interval_ms"] = tc08.usb_tc08_get_minimum_interval_ms(chandle)
      assert_pico2000_ok(status["get_minimum_interval_ms"])

# get single temperature reading
      temp = (ctypes.c_float * 9)()
      overflow = ctypes.c_int16(0)
      units = tc08.USBTC08_UNITS["USBTC08_UNITS_CENTIGRADE"]
      status["get_single"] = tc08.usb_tc08_get_single(chandle,ctypes.byref(temp), ctypes.byref(overflow), units)
      assert_pico2000_ok(status["get_single"])

# print data
#    print("Cold Junction ", temp[0]," Channel ",str(i), temp[i])
      f.write(str(temp[i]))
      if(i<len):
        f.write(", ")
      else:
        f.write("\n")
      temps[i-1]=temp[i]

      elapsed_time = time.time() - start
# close unit
#elapsed_time = time.time() - start
    print(temps[0],temps[1],temps[2],temps[3],temps[4],temps[5],temps[6],temps[7])
    x=range(0, 10, 1)
    y.insert(0, temps[0])
    y.pop(10)
    clf()
    ylim(0, 1000)
    plot(x, y)
    pause(0.05)
  
  except  KeyboardInterrupt:
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    break
# display status returns
print(status)
print("time: ",str(elapsed_time))
f.write("start time: ")
f.write(str(elapsed_time))
f.write("\n")
f.close()