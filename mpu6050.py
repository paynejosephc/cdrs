#!/usr/bin/python

import smbus2 as smbus
import math
import time

class MPU6050:
    def __init__(self):
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.address = 0x68
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
    
    def wake(self):
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

class Accel(MPU6050):
    def __init__(self):
        MPU6050.__init__(self)
        self.xout = 0
        self.yout = 0
        self.zout = 0
        self.mag = 0

    def updatexyz(self):
        self.xout = MPU6050.read_word_2c(self,0x3b)/16384.0
        self.yout = MPU6050.read_word_2c(self,0x3d)/16384.0
        self.zout = MPU6050.read_word_2c(self,0x3f)/16384.0
        self.mag = math.sqrt((self.xout*self.xout)
                             +(self.yout*self.yout)
                             +(self.zout*self.zout))

    def dist(a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)

    def getxyz(self):
        return self.xout, self.yout, self.zout
    
    def getmag(self):
        return self.mag

class Gyro(MPU6050):
    def __init__(self):
        MPU6050.__init__(self)
        self.xout = 0
        self.yout = 0
        self.zout = 0

    def updatexyz(self):
        self.xout = MPU6050.read_word_2c(self,0x43)
        self.yout = MPU6050.read_word_2c(self,0x45)
        self.zout = MPU6050.read_word_2c(self,0x47)
        

    def getxyz(self):
        return self.xout, self.yout, self.zout

        
if __name__ == "__main__":
    accel = Accel()
    gyro = Accel()
    while(True):
        gyro.updatexyz()
        accel.updatexyz()
        mag = accel.getmag()
        if mag > 3:
            print("Mag: ",mag)
            print("Accel: ", accel.getxyz())
            print("Gyro: ", gyro.getxyz())
            time.sleep(2)
        
