import csv

import mpu6050
import datetime



#myData = [["first_name", "second_name", "Grade"],
#         ['Alex', 'Brian', 'A'],
#          ['Tom', 'Smith', 'B']]
accel = mpu6050.Accel()
while(True):
    accel.updatexyz()
    x = accel.getmag()
    print(x)
    with open('accelerometer.csv', 'a') as outfile:
       
        outfile.writelines("{}, {}\n".format(x, datetime.datetime.now()))
    
    

     
print("Writing complete")
