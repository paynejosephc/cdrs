#! /usr/bin/python
# Joseph Payne - CDRS
# GPSPoller function taken from Dan Mandle http://dan.mandle.me


import os
from gps import *
from time import *
import time
import threading
from threading import Thread
from collections import deque
import datetime

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
        self.lat = ""
        self.long = ""
        self.speed = ""
        self.trigger = False
        self.buffer = deque(maxlen=30)

    def run_loop(self):
        self.getName = True
        count = -1
        while True:
            if self.trigger:
                if self.getName:
                    name = "[]".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_gps.csv"))
                    self.getName = False
                with open(name, "w+") as outfile:
                    for point in self.buffer:
                        outfile.writelines("{},{},{}\n".format(point[0],point[1],point[2]))
                count = 30
            if count >= 0:
                with open(name, 'a') as outfile:
                    outfile.writelines("{},{},{}\n".format(point[0], point[1], point[2]))
                count -= 1
            else:
                self.trigger = False
                self.getName = True

            self.lat = gpsd.fix.latitude
            self.long = gpsd.fix.longitude
            self.speed = gpsd.fix.speed

            self.datapoint = [self.lat, self.long, self.speed]

            self.buffer.append(self.datapoint)

            time.sleep(0.5)

    def start(self):
        t1 = Thread(target=self.run_loop)
        t1.setDaemon(True)
        t1.start()

    def get_gps_info(self):
        return gpsd.fix.longitude, gpsd.fix.latitude, gpsd.fix.speed

if __name__ == '__main__':
    gpsm = gps_module()
    while True:
        print(gpsm.get_gps_info())

