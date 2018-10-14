#########################################################################
# Date: 2018/10/02
# file name: 1st_assignment_main.py
# Purpose: this code has been generated for the 4 wheels drive body
# moving object to perform the project with ultra sensor
# this code is used for the student only
#########################################################################

from car import Car
import pickle
import time


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

    def drive_parking(self):
        self.car.drive_parking()

    # =======================================================================
    # 1ST_ASSIGNMENT_CODE
    # Complete the code to perform First Assignment
    # =======================================================================
    def car_startup(self):

        # setting distance variable & distance graph
        distance_graph = []
        before_distance, distance = 0, 0

        # record start time & go straight with Fastest speed
        start_time = time.time()
        self.car.accelerator.go_forward(Car.FASTEST)
        
        while True:
            distance = self.car.distance_detector.get_distance()
            distance_graph.append(distance)
            print(distance)
            
            # checking distance is lower than 10cm
            if distance <= 15:
                if before_distance - distance > 10 or distance == -1:
                    continue
                
                else:
                    break

            # assign distance for after checking distance
            before_distance = distance

        # stop car & record execution time
        self.car.accelerator.stop()
        end_time = time.time() - start_time
        time.sleep(0.8)

        # go back during end_time
        self.car.accelerator.go_backward(Car.FASTEST)
        time.sleep(end_time - 0.2)
        self.car.accelerator.stop()

        # write distance graph
        self.record_distance_log(distance_graph)

    # read distance binary log file
    def read_distance_log(self) -> object:
        with open("distance_log.dat", "rb") as log_file:
            distance_trace = pickle.load(log_file)
            
            for log in distance_trace:
                print(log)
    
    def record_distance_log(self, distance_log: list):
        with open("distance_log.dat", "rb") as log_file:
            distance_list = pickle.load(log_file)
            
        with open("distance_log.dat", "wb") as log_file:
            distance_list.append(distance_log)
            pickle.dump(distance_list, log_file)
        
if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
