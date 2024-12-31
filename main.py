import os
import requests
from network_connect import connectNetwork
from train_api.route import Route
from train_api.client import TrainClient
import time
from ntptime import settime
from datetime import datetime
from machine import Pin, SPI
import epaper7in3f
import framebuf
import ubinascii
import config

time_offset = - 6 * 3600

train_key = "e7f78bf618fc46cd9f6ea3e1eb3c9ca9"

route = Route.BLUE
station_name = "Grand"

wlan = connectNetwork()
time.sleep(2)
print("setting time")
while True:
    try:
        settime()
        print("Time success")
        break
    except:
        print("Time failed, trying again")
        continue

config_or_read = input("Create new config? (y/N) : \n")
if config_or_read.lower()=='y':
    cfg = config.prompt_config()
else:
    cfg =  config.read_config()

client = TrainClient(train_key)
while True:
    entries = []
    for stop in cfg:
        stpid = int(stop['stop_id'])
        etas = client.arrivals(stpid=stpid)['ctatt']['eta']
        for eta in etas:
            curr_time = time.time() + time_offset
            arr_time = datetime.fromisoformat(eta["arrT"])
            diff = round((time.mktime(arr_time.timetuple()) - curr_time)/60)
            stop_text = "%s: %s (%s)"% (eta['rt'], eta['staNm'], eta['destNm'])
            entries.append( (stop_text, diff, eta['isApp']) )

    sorted_entries = sorted(entries, key=lambda entry: entry[1])
    for (stop, eta, is_app) in sorted_entries:
        print_str = "%s: %d mins" %(stop, eta)
        if (is_app):
            print_str.upper()
        print(print_str)

    print("---------------------------------")

#print("setuping up spi")
#spi = SPI(1, baudrate=2000000, polarity=0, phase=0)
#cs = Pin(27)
#dc = Pin(26)
#rst = Pin(25)
#busy = Pin(33)
#print("setup spi")
#
#print("setuping up epaper")
#e = epaper7in3f.EPD(spi, cs, dc, rst, busy)
#e.init()
#print("setup epaper")
#
#
#w = 800
#h = 100
#x = 0
#y = 0
#
#print("writing  black")
#e.fill_frame(b'\x00')
#print("writing  white")
#e.fill_frame(b'\x11')
#print("writing  green")
#e.fill_frame(b'\x22')
#print("writing  blue")
#e.fill_frame(b'\x33')
#print("writing  red")
#e.fill_frame(b'\x44')
#print("writing  yelow")
#e.fill_frame(b'\x55')
#print("writing  orange")
#e.fill_frame(b'\x66')
