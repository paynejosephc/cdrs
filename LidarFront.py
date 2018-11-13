__version__ = '0.1'
import serial
import time
import csv
from itertools import zip_longest
from queue import Queue
import datetime
from threading import Thread


class LidarFront:
    def __init__(self):
        self.Rear_Dist = Queue(30)
        self.TimeStamp = Queue(30)
        self.DataD = []
        self.DataT = []
        self.trigger = False
        print("check")

    def run_loop(self):
        n = 0
        number_rows = 0
        while True:

            time.sleep(.45)
            ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)  

            ser.write(bytes(b'B'))

            ser.write(bytes(b'W'))

            ser.write(bytes(2))

            ser.write(bytes(0))

            ser.write(bytes(0))

            ser.write(bytes(0))
                      
            ser.write(bytes(1))
                      
            ser.write(bytes(6))



            Dist_Total = 0
           
                
            if((b'Y' == ser.read()) and ( b'Y' == ser.read())):
                
                Dist_L = ser.read()
                Dist_H = ser.read()
                Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
                print(str(Dist_Total) + ' cm')
                
                if(self.trigger == True):
                    
                    if n ==0:
                        
                        i = 0
                        j = self.Rear_Dist.qsize()
                        while i < j:         
                            self.DataD.append(self.Rear_Dist.get(i))
                            self.DataT.append(self.TimeStamp.get(i))
                            i = i +1
                              
                        self.Data = [self.DataT,self.DataD]
                        Export_Data = zip_longest(*self.Data, fillvalue = '')

                        with open('LidarFront1.csv', "w", encoding = "ISO-8859-1", newline='') as csv_file:
                            writer = csv.writer(csv_file, delimiter=',')
                            writer.writerows(Export_Data)
                            csv_file.close()
                            n = 1
                    
                    if n ==1:
                        self.DataD[1:] =[]
                        self.DataT[1:] =[]
                        self.DataD[0] = Dist_Total
                        self.DataT[0] = datetime.datetime.now()
                        
                        self.Data = [self.DataT,self.DataD]
                        Export_Data = zip_longest(*self.Data, fillvalue = '')
                        print(self.Data)

                        with open('LidarFront1.csv', "a", encoding = "ISO-8859-1", newline='') as csv_file:
                            writer = csv.writer(csv_file, delimiter=',')
                            writer.writerows(Export_Data)
                            csv_file.close()


                if(self.trigger == False):
                    if self.Rear_Dist.qsize() >= 30:
                        self.Rear_Dist.get(0,1)
                        self.TimeStamp.get(0,1)
                    self.Rear_Dist.put(Dist_Total)
                    self.TimeStamp.put(datetime.datetime.now())
            


    def start(self):

        t1 = Thread(target=self.run_loop)
        t1.setDaemon(True)
        t1.start()

    def set_trigger(self):
        print("Trigger...")
        print(datetime.datetime.now())
        self.trigger = True
        print("Sleep...")
        time.sleep(15)
        print("Un-trigger...")
        print(datetime.datetime.now())
        self.trigger = False



if __name__ == "__main__":

    Front = LidarFront()
    Front.start()
    time.sleep(20)
    Front.set_trigger()
    #print('checking')
    
