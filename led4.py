import time 
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
y = 25
g = 18
GPIO.setup(y, GPIO.OUT)
GPIO.setup(g, GPIO.OUT)
blink_num = int(input("How many blinks would you like? "))
for i in range(0, blink_num):
	GPIO.output(y, True)
	time.sleep(.2)
	GPIO.output(y, False)
	time.sleep(.2)
	GPIO.output(g, True)
	time.sleep(.2)
	GPIO.output(g, False)
	time.sleep(.2)
GPIO.cleanup()
