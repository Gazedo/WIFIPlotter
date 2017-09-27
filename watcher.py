#!/usr/bin/env python3

import serial
import pyinotify
import asyncio
import os

ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)
wm.add_watch('/home/pi/Print', pyinotify.ALL_EVENTS)

def send_to_serial(stuff1, stuff2):
    path = '/home/pi/Print'
    files = [f for f in os.listdir(path) if os.path.isfile(path + f) and (f.endswith('hpgl') or f.endswith('plt'))]
    for f in files:
        in_file = open(f, 'r')
        ser.write(in_file.encode())
        in_file.close()
        os.remove(path + f)

try:
    notifier.loop(daemonize=True, callback=send_to_serial, pid_file='/tmp/pyinotify.pid', stdout='/tmp/pyinotify.log')
except pyinotify.NotifierError, err:
    print >> sys.stderr, err

