"""
"""
import obd
import datetime
import time
from threading import Thread
from collections import deque
#obd.logger.setLevel(obd.logging.DEBUG)

class obdii:
    def __init__(self):
        self.speed = 0
        self.throttle = 0
        self.rpm = 0
        self.mil = 0
        self._trigger = False
        self.buffer = deque(maxlen = 30)
        self.datapoint = 0
        self.connection = obd.OBD()
        self.start()

    def run_loop(self):
        #connection = obd.OBD()
        self.speed_cmd = obd.commands.SPEED
        self.throttle_cmd = obd.commands.THROTTLE_POS
        self.rpm_cmd = obd.commands.RPM
        self.mil_cmd = obd.commands.DISTANCE_W_MIL
        count = -1
        get_name = True

        while(True):
            if self._trigger:
                #opens the out file
                if get_name:
                    name = '/home/pi/data/{event_time}'.format(
                    event_time=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S_obd.csv')
                    )
                    get_name = False
                with open(name, "w+") as out_file:
                    #writes every line to a file
                    for point in self.buffer:
                        out_file.writelines("{}, {}, {}, {}, {}\n".format(point[0], point[1], point[2], point[3],point[4]))
                count = 30
            if count >= 0:
                with open(name, "a") as out_file:
                    out_file.writelines("{}, {}, {}, {}, {}\n".format(self.datapoint[0], self.datapoint[1], self.datapoint[2], self.datapoint[3],self.datapoint[4]))
                count -= 1
            else:
                self._trigger = False
                get_name = True
                    

            #calls a parameter from the vehicle
            self.speed_response = self.connection.query(self.speed_cmd)
            self.throttle_response = self.connection.query(self.throttle_cmd)
            self.rpm_response = self.connection.query(self.rpm_cmd)
            self.mil_response = self.connection.query(self.mil_cmd)

            #prints the value called from query
            #print(self.speed_response.value)
            #print(self.throttle_response.value)
            #print(self.rpm_response.value)
            #print(self.mil_response.value)
            
            #takes all four parameter values and stores them as a set
            self.datapoint = [str(datetime.datetime.now()), self.speed_response.value, self.throttle_response.value, self.rpm_response.value, self.mil_response.value]

            #appends it to the buffer
            self.buffer.append(self.datapoint)

            #pause before looping again and sets frequency
            #cycing every 0.5sec, which is 2x per second, which is 2Hz
            time.sleep(0.5)

    def start(self):
        t1 = Thread(target=self.run_loop)
        t1.setDaemon(True)
        t1.start()

    def trigger(self):
        self._trigger = True
        time.sleep(15)
        self._trigger = False

if __name__ == "__main__":
    car = obdii()
    car.start()
    print("Starting car")
    time.sleep(20)
    print("Triggering")
    car.trigger()
    print("Done")

    

