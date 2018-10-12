#########################################################################
# Date: 2018/10/02
# file name: car.py
# Purpose: this code has been generated for the 4 wheels drive body
# this code is used for the student only
#########################################################################


# =======================================================================
# import GPIO library and time module
# =======================================================================
import RPi.GPIO as GPIO

# =======================================================================
# import ALL method in the SEN040134 Tracking Module
# =======================================================================
from SEN040134 import SEN040134_Tracking as Tracking_Sensor

# =======================================================================
# import ALL method in the TCS34725 RGB Module
# =======================================================================
from TCS34725 import TCS34725_RGB as RGB_Sensor

# =======================================================================
# import ALL method in the SR02 Ultrasonic Module
# =======================================================================
from SR02 import SR02_Supersonic as Supersonic_Sensor

# =======================================================================
# import ALL method in the PCA9685 Module
# =======================================================================
from PCA9685 import PCA9685 as PWM_Controller

# =======================================================================
# import ALL method in the rear/front Motor Module
# =======================================================================
import rear_wheels
import front_wheels

# =======================================================================
#  set GPIO warnings as false
# =======================================================================
GPIO.setwarnings(False)


class Car(object):

    """ Initialize Speed Value """
    SLOWEST = 20
    SLOWER = 25
    SLOW = 35
    NORMAL = 40
    FAST = 65
    FASTER = 80
    FASTEST = 100

    def __init__(self, carName: str):
        file = open("driver_log.txt")
        # ================================================================
        # ULTRASONIC MODULE DRIVER INITIALIZE
        # ================================================================
        try:
            self.distance_detector = Supersonic_Sensor.Supersonic_Sensor(35)
            file.write("ULTRASONIC MODULE DRIVER : OK\n")

        except:
            file.write("ULTRASONIC MODULE DRIVER : ERROR\n")
        # ================================================================
        # TRACKING MODULE DRIVER INITIALIZE
        # ================================================================
        try:
            self.line_detector = Tracking_Sensor.SEN040134_Tracking([16, 18, 22, 40, 32])
            file.write("TRACKING MODULE DRIVER : OK\n")

        except:
            file.write("TRACKING MODULE DRIVER : ERROR\n")

        # ================================================================
        # PCA9685(PWM 16-ch Extension Board) MODULE WAKEUP
        # ================================================================
        try:
            self.carEngine = PWM_Controller.PWM()
            self.carEngine.startup()
            file.write("PCA9685 MODULE DRIVER : OK\n")

        except:
            file.write("PCA9685 MODULE WAKEUP : ERROR\n")

        # ================================================================
        # FRONT WHEEL DRIVER SETUP
        # ================================================================
        try:
            self.steering = front_wheels.Front_Wheels(db='config')
            self.steering.ready()
            file.write("FRONT WHEEL DRIVER : OK\n")

        except:
            file.write("FRONT WHEEL DRIVER : ERROR\n")

        # ================================================================
        # REAR WHEEL DRIVER SETUP
        # ==================================================6==============
        try:
            self.accelerator = rear_wheels.Rear_Wheels(db='config')
            self.accelerator.ready()
            file.write("REAR WHEEL DRIVER SETUP : OK\n")

        except:
            file.write("REAR WHEEL DRIVER SETUP : ERROR\n")

        # ================================================================
        # SET LIMIT OF TURNING DEGREE
        # ===============================================================
        self.steering.turning_max = 35

        # ================================================================
        # SET FRONT WHEEL CENTOR ALLIGNMENT
        # ================================================================
        self.steering.center_alignment()

        # ================================================================
        # SET APPOINTED OF CAR NAME
        # ================================================================
        self.car_name = carName
        '''
        except Exception as e:
            print("CONTACT TO Kookmin Univ. Teaching Assistant")
            print("Learn more : " + e)
        '''
        file.close()

    def drive_parking(self):
        # front wheels center alignment
        self.steering.center_alignment()

        # power down both wheels
        self.accelerator.stop()
        self.accelerator.power_down()

        # GPIO clean up
        GPIO.cleanup()