import serial
import time
import RPi.GPIO as GPIO

LEDpin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LEDpin,GPIO.OUT)
GPIO.output(LEDpin,GPIO.LOW)

ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 1)
print(ser)

#ser.write(0x42)
ser.write(bytes(b'B'))

#ser.write(0x57)
ser.write(bytes(b'W'))

#ser.write(0x02)
ser.write(bytes(2))

#ser.write(0x00)
ser.write(bytes(0))

#ser.write(0x00)
ser.write(bytes(0))

#ser.write(0x00)
ser.write(bytes(0))
          
#ser.write(0x01)
ser.write(bytes(1))
          
#ser.write(0x06)
ser.write(bytes(6))


Dist_Total = 0
j = 0

while(True):
    
    while(ser.in_waiting >= 9):
        while( j == 100):
            print (ser.read())
            print(Dist_Total)
            j =0
        
        if((b'Y' == ser.read()) and ( b'Y' == ser.read())):
            
            GPIO.output(LEDpin, GPIO.LOW)
            Dist_L = ser.read()
            Dist_H = ser.read()
            Dist_Total = (ord(Dist_H) * 256) + (ord(Dist_L))
            for i in range (0,5):
                ser.read()
        j += 1        
        if(Dist_Total < 20):
            GPIO.output(LEDpin, GPIO.HIGH)


        
