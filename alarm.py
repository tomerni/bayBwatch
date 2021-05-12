import RPi.GPIO as GPIO
from time import sleep
import time


def switch_alarm():
    """
    connects to the alarm and switches it to the state provided as an argument
    :return: True if completed successfully
    """
    GPIO.setwarnings(False)
    print("alarm is on")
    GPIO.setmode(GPIO.BCM)
    buzzer = 18  # the number of the connection
    GPIO.setup(buzzer, GPIO.OUT)
    t_end = time.time() + 15
    while time.time() < t_end: # TODO: change condition to adult detection
        GPIO.output(buzzer, GPIO.HIGH)
        print("Beep")
        sleep(0.5)
        GPIO.output(buzzer, GPIO.LOW)
        print("No Beep")
        sleep(0.5)


