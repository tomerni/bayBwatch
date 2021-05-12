#import RPi.GPIO as GPIO
from time import sleep
import time
import threading

from shapely.geometry import Point, Polygon

pool_poly = None

to_work = [1]

def switch_alarm():
    """
    connects to the alarm and switches it to the state provided as an argument
    :return: True if completed successfully
    """
    #GPIO.setwarnings(False)
    print("alarm is on")
    #GPIO.setmode(GPIO.BCM)
    buzzer = 18  # the number of the connection
    #GPIO.setup(buzzer, GPIO.OUT)
    t_end = time.time() + 15
    while to_work[0]: # TODO: change condition to adult detection
        #GPIO.output(buzzer, GPIO.HIGH)
        print("Beep")
        sleep(0.5)
        #GPIO.output(buzzer, GPIO.LOW)
        print("No Beep")
        sleep(0.5)


th = threading.Thread(target=switch_alarm)


def check_borders(child_coords):
    # create a point out of the coords
    child_x = child_coords[0]
    child_y = 720 - child_coords[1] # 720 is the height of a RPi camera image
    child_point = Point(24.952242, 60.1696017)
    return child_point.within(pool_poly)
