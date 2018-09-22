#!/usr/bin/python

""" This is the main file for the Wrech Tech Team's Crash Data Recording System
(CDRS) unit. This file will be run as a service on startup of the RPi """

import time

# Start up OBDII

# Start up LiDAR 0

# Start up LiDAR 1

# Start up camera 0

# Start up camera 1

# Start up GPS

# Start up the Accelerometer code

impact_magnitude = 0

while(True):
    impact_magnitude = 0 # accel.getmag() #get the magnitude of the acceleration

    if impact_magnitude >= 3.0:
        # trigger Camera 0

        # trigger Camera 1

        # trigger LiDAR 0

        # trigger LiDAR 1

        # trigger OBDII

        # trigger GPS

        time.sleep(15)


        
