# Crash Data Recording System

This code was developed by the Wrech Tech Electrical Engineering Senior Design Team at Mississippi State University. 

The primary contributor of the code was me, Joseph Payne [@paynejosephc](https://github.com/paynejosephc/), with additional contributions from William Mathis (lidar interface) and Brandon Gill (camera interface). 

## How to use:

This was written to run on a Raspberry Pi with PIGPIO installed. 
Run the `main_combo.py` file. This will start a task for the sensors and record the data the `/home/pi/data/` folder. 
##### Note: the main.py file works, but not on a RPi as it spawns too many threads. 
