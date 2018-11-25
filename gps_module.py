#! /usr/bin/python
# Joseph Payne - CDRS
# GPSPoller function taken from Dan Mandle http://dan.mandle.me


import os
from gps import *
from time import *
import time
import threading

gpsd = None  # seting the global variable

os.system('clear')  # clear the terminal (optional)


class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd  # bring it in scope
        gpsd = gps(mode=WATCH_ENABLE)  # starting the stream of info
        self.current_value = None
        self.running = True  # setting the thread running to true

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()  # this will continue to loop and grab EACH set of gpsd info to clear the buffer


class gps_module:
    def __init__(self):
        gpsp = GpsPoller()
        gpsp.start()

    def get_gps_info(self):
        return gpsd.fix.longitude, gpsd.fix.latitude, gpsd.fix.speed

if __name__ == '__main__':
    gpsm = gps_module()
    while True:
        print(gpsm.get_gps_info())

