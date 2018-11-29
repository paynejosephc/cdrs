#! /usr/bin/python
# Joseph Payne - CDRS
# GPSPoller function taken from Dan Mandle http://dan.mandle.me


import os
from gps import *
import gpsd
from time import *
import time
import threading
from threading import Thread
from collections import deque
import datetime

#TODO add no fix handling

class gps_module:
    def __init__(self):
        gpsd.connect()
        self.lat = ""
        self.long = ""
        self.speed = ""
        self._trigger = False
        self.buffer = deque(maxlen=30)
        self.start()

    def run_loop(self):
        self.getName = True
        count = -1
        while True:
            if self._trigger:
                if self.getName:
                    name = "/home/pi/data/{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_gps.csv"))
                    self.getName = False
                with open(name, "w+") as outfile:
                    for point in self.buffer:
                        outfile.writelines("{},{},{},{}\n".format(point[0],point[1],point[2],point[3]))
                count = 30
            if count >= 0:
                with open(name, 'a') as outfile:
                    outfile.writelines("{},{},{},{}\n".format(point[0], point[1], point[2],point[3]))
                count -= 1
            else:
                self._trigger = False
                self.getName = True
            fix = gpsd.get_current()
            timenow = str(datetime.datetime.now())
            self.lat = fix.position()[0]
            self.long = fix.position()[1]
            self.speed = fix.speed()

            self.datapoint = [timenow,self.lat, self.long, self.speed]

            self.buffer.append(self.datapoint)

            time.sleep(0.5)

    def start(self):
        t1 = Thread(target=self.run_loop)
        t1.setDaemon(True)
        t1.start()

    def trigger(self):
        self._trigger = True
        time.sleep(15)
        self._trigger = False

if __name__ == '__main__':
    gpsm = gps_module()
    #gpsm.start()
    time.sleep(20)
    gpsm.trigger()
    


