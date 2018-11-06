#!/usr/bin/python

""" This is the main file for the Wrech Tech Team's Crash Data Recording System
(CDRS) unit. This file will be run as a service on startup of the RPi """
debug = True
def debug(debugtext):
    if debug:
        print(debugtext)
        
import time
from mpu6050 import Accel

# Start up OBDII
debug("Starting OBDII interface...")

# Start up LiDAR 0
debug("Starting front lidar interface...")

# Start up LiDAR 1
debug("Starting rear lidar interface...")

# Start up camera 0
debug("Starting front camera interface...")

# Start up camera 1
debug("Starting rear camera interface...")

# Start up GPS
debug("Starting GPS inteface...")

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

        # trigger Camera 1
        debug("TRIGGER: rear camera")

        # trigger LiDAR 0
        debug("TRIGGER: front lidar")

        # trigger LiDAR 1
        debug("TRIGGER: rear lidar")

        # trigger OBDII
        debug("TRIGGER: OBDII")

        # trigger GPS
        debug("TRIGGER: GPS")

        debug("Waiting 15 for sensor data to stop writing to file..")
        time.sleep(15)
        debug("Returning to monitoring...")


        