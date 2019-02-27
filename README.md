# Crash Data Recording System

This code was developed by the Wrech Tech Electrical Engineering Senior Design Team at Mississippi State University. 
Website: https://design.ece.msstate.edu/2018/team_payne/

The primary contributor of the code was me, Joseph Payne [@paynejosephc](https://github.com/paynejosephc/), with additional contributions from William Mathis (lidar interface) and Brandon Gill (camera interface). 

Detailed documentation for product design process can be found here: https://design.ece.msstate.edu/2018/team_payne/documents.html

## How to use:
Specsheets on hardware used are available here: https://design.ece.msstate.edu/2018/team_payne/datasheets.html
This was written to run on a Raspberry Pi with PIGPIO installed. 
Run the `main_combo.py` file. This will start a task for the sensors and record the data the `/home/pi/data/` folder. 
**Note: the `main.py` file works, but not on a RPi as it spawns too many threads.**

