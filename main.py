#!/usr/bin/python

""" This is the main file for the Wrech Tech Team's Crash Data Recording System
(CDRS) unit. This file will be run as a service on startup of the RPi """
debug_bool = True
def debug(debugtext):
    if debug_bool:
        print(debugtext)
        
import time
from mpu6050 import Accel
from recorder import Sentry
from gps_module import gps_module
from threading import Thread
from LidarFront import LidarFront
from LidarRear import LidarRear
from obdii import obdii

# Start up OBDII
debug("Starting OBDII interface...")
#obd = obdii()

# Start up LiDAR 0
debug("Starting front lidar interface...")
lid0 = LidarFront()

# Start up LiDAR 1
debug("Starting rear lidar interface...")
lid1 = LidarRear()

# Start up camera 0
debug("Starting front camera interface...")
cam0 = Sentry(name = "front", verbose=True)

# Start up camera 1
debug("Starting rear camera interface...")
cam1 = Sentry(name = "rear", src=1)

# Start up GPS
debug("Starting GPS inteface...")
gps = gps_module()

# Start up the Accelerometer code
debug("Starting Accelerometer interface...")
acc = Accel()

impact_magnitude = 0
debug("Starting Monitor Loop...")
while(True):
    acc.updatexyz()
    impact_magnitude = acc.getmag() #get the magnitude of the acceleration

    if impact_magnitude >= 3.0:
        debug("Accel Magnitude: {}".format(impact_magnitude))
        # trigger Camera 0
        debug("TRIGGER: front camera")
        cam0_t = Thread(target=cam0.set_trigger)
        cam0_t.start()
        
        # trigger Camera 1
        debug("TRIGGER: rear camera")
        cam1_t = Thread(target=cam1.set_trigger)
        cam1_t.start()

        # trigger LiDAR 0
        debug("TRIGGER: front lidar")
        lid0_t = Thread(target=lid0.set_trigger)
        lid0_t.start()

        # trigger LiDAR 1
        debug("TRIGGER: rear lidar")
        lid1_t = Thread(target=lid1.set_trigger)
        lid1_t.start()

        # trigger OBDII
        debug("TRIGGER: OBDII")
        #obd_t = Thread(target=obd.trigger)
        #odd_t.start()

        # trigger GPS
        debug("TRIGGER: GPS")
        gps_t = Thread(target=gps.trigger)
        gps_t.start()


        debug("Waiting 15 for sensor data to stop writing to file..")
        time.sleep(15)
        debug("Returning to monitoring...")


        
