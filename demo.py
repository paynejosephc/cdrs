""" Demo Mode for the CDRS """

import obd
import datetime
import time
from threading import Thread
import gpsd
import serial
from recorder import Sentry

class data:
    def __init__(self):
        self.connection = 0

        self.speed = 0
        self.throttle = 0
        self.rpm = 0
        self.lat = 0
        self.long = 0
        self.GPSspeed = 0
        self.front_dist = 0
        self.rear_dist = 0

        self.speed_cmd = obd.commands.SPEED
        self.throttle_cmd = obd.commands.THROTTLE_POS
        self.rpm_cmd = obd.commands.RPM
        self.mil_cmd = obd.commands.DISTANCE_W_MIL

    def connect(self):
        self.connection = obd.OBD()
        gpsd.connect()

    def update_dataframe(self):
        fix = gpsd.get_current()
        self.speed = self.connection.query(self.speed_cmd).value
        self.throttle = self.connection.query(self.throttle_cmd).value
        self.rpm = self.connection.query(self.rpm_cmd).value

        self.lat = fix.position()[0]
        self.long = fix.position()[1]
        self.GPSspeed = fix.speed()

        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        ser.write(bytes(b'B'))

        ser.write(bytes(b'W'))

        ser.write(bytes(2))

        ser.write(bytes(0))

        ser.write(bytes(0))

        ser.write(bytes(0))

        ser.write(bytes(1))

        ser.write(bytes(6))

        if ((b'Y' == ser.read()) and (b'Y' == ser.read())):
            Dist_L = ser.read()
            Dist_H = ser.read()
            self.front_dist = (ord(Dist_H) * 256) + (ord(Dist_L))

        ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)

        ser.write(bytes(b'B'))

        ser.write(bytes(b'W'))

        ser.write(bytes(2))

        ser.write(bytes(0))

        ser.write(bytes(0))

        ser.write(bytes(0))

        ser.write(bytes(1))

        ser.write(bytes(6))

        if ((b'Y' == ser.read()) and (b'Y' == ser.read())):
            Dist_L = ser.read()
            Dist_H = ser.read()
            self.rear_dist = (ord(Dist_H) * 256) + (ord(Dist_L))

        print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(self.speed, self.throttle, self.rpm, self.lat, self.long, self.GPSspeed, self.front_dist, self.front_dist))

if __name__ == "__main__":
    d = data()
    d.connect()
    update_t = Thread(target=d.update_dataframe)
    cam0 = Sentry(name="front",verbose=True)
    cam1 = Sentry(name="rear",src=1,verbose=True)
    update_t.start()
