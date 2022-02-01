import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

GPIO.output(12, GPIO.TRUE)
time.sleep(2)

GPIO.output(12, GPIO.FALSE)

GPIO.cleanup()

