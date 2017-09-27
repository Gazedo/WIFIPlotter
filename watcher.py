#!/usr/bin/env python3

import serial
import pyinotify
import asyncio
import os
import time

def send_to_serial(stuff1):
    print(stuff1)
    path = '/home/pi/Print/'
    files = [f for f in os.listdir(path) if os.path.isfile(path + f) and (f.endswith('hpgl') or f.endswith('plt'))]
    print(files)
    for f in files:
        in_file = open(path + f, 'r')
        ser.write(in_file.encode())
        print('found {}'.format(f))
        in_file.close()
        os.remove(path + f)
        notifier.loop.stop()

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
loop = asyncio.get_event_loop()
notifier = pyinotify.AsyncioNotifier(wm, loop, callback=send_to_serial)
wm.add_watch('/home/pi/Print', pyinotify.IN_CLOSE_WRITE)
print('Added watch')
loop.run_forever()
notifier.stop()

# notifier.loop(daemonize=True, callback=send_to_serial, pid_file='/tmp/pyinotify.pid', stdout='/tmp/pyinotify.log')
# while True:
    # notifier.loop(callback=send_to_serial, stdout='/tmp/watcher.log')
    # time.sleep(10)
    # print('Setup up notifier')

