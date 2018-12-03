
import os
from gps import *
import gpsd
from time import *
import time
import obd
import datetime
from threading import Thread
from collections import deque
#obd.logger.setLevel(obd.logging.DEBUG)


#TODO add no fix handling

class combo:
    def __init__(self):
        gpsd.connect()
        self.lat = ""
        self.long = ""
        self.speed = ""
        self.GPSspeed = 0
        self.throttle = 0
        self.rpm = 0
        self.mil = 0
        self.datapoint = 0
        self.connection = obd.OBD()
        self._trigger = False
        self.buffer = deque(maxlen=30)
        self.start()

    def run_loop(self):
        self.speed_cmd = obd.commands.SPEED
        self.throttle_cmd = obd.commands.THROTTLE_POS
        self.rpm_cmd = obd.commands.RPM
        self.mil_cmd = obd.commands.DISTANCE_W_MIL
        self.getName = True
        count = -1

        while True:
            if self._trigger:
                if self.getName:
                    name = "/home/pi/data/{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_obd_gps.csv"))
                    self.getName = False
                with open(name, "a") as outfile:
                    outfile.writelines("TimeStamp, Latitude, Longitude, GPS Speed, OBD Speed, Throttle Pos., RPM, MIL Status\n")
                    for point in self.buffer:
                        outfile.writelines("{},{},{},{},{},{},{},{}\n".format(point[0],point[1],point[2],point[3],point[4],point[5],point[6],point[7]))
                count = 30
            if count >= 0:
                with open(name, 'a') as outfile:
                    outfile.writelines("{},{},{},{},{},{},{},{}\n".format(self.datapoint[0],self.datapoint[1],self.datapoint[2],self.datapoint[3],self.datapoint[4],self.datapoint[5],self.datapoint[6],self.datapoint[7]))
                count -= 1
            else:
                self._trigger = False
                self.getName = True

            # calls a parameter from the vehicle
            self.speed_response = self.connection.query(self.speed_cmd)
            self.throttle_response = self.connection.query(self.throttle_cmd)
            self.rpm_response = self.connection.query(self.rpm_cmd)
            self.mil_response = self.connection.query(self.mil_cmd)

            fix = gpsd.get_current()
            timenow = str(datetime.datetime.now())
            self.lat = fix.position()[0]
            self.long = fix.position()[1]
            self.speed = fix.speed()

            self.datapoint = [timenow, self.lat, self.long, self.GPSspeed, self.speed_response.value, self.throttle_response.value, self.rpm_response.value, self.mil_response.value]

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
