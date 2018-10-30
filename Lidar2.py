import serial
import time
import csv
from itertools import zip_longest
from queue import Queue
import datetime


Rear_Dist = Queue(20)
#Rear_Dist = []
TimeStamp = Queue(20)
DataD = []
DataT = []


T = False
j =0
n = 0
while(True):

    if j < 20:
        j= j+1
        
    if j == 20:
        T = True

    time.sleep(.5)
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
        
        if((T == True) & (n == 0) ):
            
            i = 0
            while i < 10:
                DataD.append(Rear_Dist.get(i))
                DataT.append(TimeStamp.get(i))

                i = i +1
            print(DataD)
            print(DataT)
                
            Data = [DataT,DataD]
            Export_Data = zip_longest(*Data, fillvalue = '')
            print(Data)
            with open('Lidar1.csv', "w", encoding = "ISO-8859-1", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                print('check')
                print(Data)
                writer.writerows(Export_Data)
                csv_file.close()
                n = 1
    
        if(T == False):
            #if(len(Rear_Dist) >= 10):
            if(Rear_Dist.qsize() >= 10):
                #print (str(Rear_Dist.remove[0]) + ' dequeued' )
                print(str(Rear_Dist.get(0)) + ' dequeued')
            Rear_Dist.put(Dist_Total)
            TimeStamp.put(datetime.datetime.now())
        
        
        
    
               
      


        
