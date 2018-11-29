__version__ = '0.1'
import serial
import time
import csv
from itertools import zip_longest
from queue import Queue
import datetime
from threading import Thread


class LidarRear:
    def __init__(self):
        self.Rear_Dist = Queue(465)
        self.TimeStamp = Queue(465)
        self.DataD = []
        self.DataT = []
        self.trigger = False
        self.event_time = None
        self.start()
        
    def run_loop(self):
        n = 0
        number_rows = 0
        while True:

            time.sleep(.02)
            ser = serial.Serial('/dev/ttyUSB1',115200,timeout = 1)  

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
                #print(str(Dist_Total) + ' cm')
                
                if(self.trigger == True):

                    #runs one time after trigger goes True
                    if n ==0:

                        #appends distance and time stamp to seperate list
                        i = 0
                        j = self.Rear_Dist.qsize()
                        while i < j:         
                            self.DataD.append(self.Rear_Dist.get(i))
                            self.DataT.append(self.TimeStamp.get(i))
                            i = i +1
                        #combines and zips distance and timestamp data      
                        self.Data = [self.DataT,self.DataD]
                        Export_Data = zip_longest(*self.Data, fillvalue = '')

                        #creates file with timestamp and writes data
                        self.event_time = datetime.datetime.now()
                        name = '/home/pi/data/{event_time}'.format(
                            event_time = self.event_time.strftime('%Y-%m-%d_%H-%H-%S_RLidar.csv'))

                        with open(name, "w", encoding = "ISO-8859-1", newline='') as csv_file:
                            writer = csv.writer(csv_file, delimiter=',')
                            writer.writerows(Export_Data)
                            csv_file.close()
                            n = 1

                    #appends file for the 15 seconds after trigger
                    if n ==1:
                        self.DataD[1:] =[]
                        self.DataT[1:] =[]
                        self.DataD[0] = Dist_Total
                        self.DataT[0] = datetime.datetime.now()
                        
                        self.Data = [self.DataT,self.DataD]
                        Export_Data = zip_longest(*self.Data, fillvalue = '')
                        #print(self.Data)

                        with open(name, "a", encoding = "ISO-8859-1", newline='') as csv_file:
                            writer = csv.writer(csv_file, delimiter=',')
                            writer.writerows(Export_Data)
                            csv_file.close()

                #manages queue to maintain a 15-16 second buffer
                if(self.trigger == False):
                    if self.Rear_Dist.qsize() >= 465:
                        self.Rear_Dist.get(0,1)
                        self.TimeStamp.get(0,1)
                    self.Rear_Dist.put(Dist_Total)
                    self.TimeStamp.put(datetime.datetime.now())
            


    def start(self):

        t2 = Thread(target=self.run_loop)
        t2.setDaemon(True)
        t2.start()

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

    Rear = LidarRear()
    Rear.start()
    time.sleep(20)
    Rear.set_trigger()
    #print('checking')
    
