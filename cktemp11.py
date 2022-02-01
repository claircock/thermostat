import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from math import *

#DHT11 setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

#setmode
GPIO.setmode(GPIO.BCM)

#my variable gpio pin assignments
W = 12
G = 18
O = 20
Y = 25
FAN = 16
HEAT = 24
COOLING = 23
EMHEAT= 13

#assign GPIO's as outputs
GPIO.setup(W, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(O, GPIO.OUT)
GPIO.setup(Y, GPIO.OUT)
GPIO.setup(FAN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(HEAT,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(COOLING,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(EMHEAT,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#using adafruitDHT code convert to a temp in C and F 
ctemp = '{0:0.1f}'.format(temperature)
ftemp = floor(float(ctemp)*1.8) + 32
#hum = '{1:0.1f}%'.format(humidity)  


#start


#Current humidity is: " + str(hum)) <---not working

def pin24_handler(pin):
	while True :
		try :
			DHT_SENSOR = Adafruit_DHT.DHT11
			DHT_PIN = 4
			humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
			ctemp2 = '{0:0.1f}'.format(temperature)
			ftemp2 = floor(float(ctemp2)*1.8) + 32
			tempdif2 = stemp - int(ftemp2)
			print("\nHeating mode activated, current temperature is: " + str(ftemp2) + " Fahirenhit")
			print("set point is " + str(stemp))
			time.sleep(10)
			if tempdif2 > 0 :
				print("System Heating")
				GPIO.output(G, True) 
				GPIO.output(Y, True)

			elif tempdif2 <= 0 :
				print("temperature setpoint met")
				GPIO.output(G, False)
				GPIO.output(Y, False)
				GPIO.output(W, False)
				GPIO.output(O, False)
				time.sleep(60)
		except :
			print("\nNo responce from DHT")
			pin24_handler
			time.sleep(5)

def pin23_handler(pin):
	while True :
		DHT_SENSOR = Adafruit_DHT.DHT11
		DHT_PIN = 4
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		ctemp2 = '{0:0.1f}'.format(temperature)
		ftemp2 = floor(float(ctemp2)*1.8) + 32
		tempdif2 = stemp - float(ftemp2)
		print("\nCooling mode activated, current temperature is: " + str(ftemp2) + " Fahrenheit")
		print("setpoint is " + str(stemp))
		time.sleep(10)
		if  tempdif2 < 0 :
			print("System Cooling")
			GPIO.output(G, True)
			GPIO.output(Y, True)
			GPIO.output(O, True)

		elif tempdif2 >= 0 :
			print("done")
			GPIO.output(G, False)
			GPIO.output(Y, False)
			GPIO.output(O, False)
			GPIO.output(W, False)


def pin13_handler(pin) :
	while True :
		DHT_SENSOR = Adafruit_DHT.DHT11
		DHT_PIN = 4
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		ctemp2 = '{0:0.1f}'.format(temperature)
		ftemp2 = floor(float(ctemp2)*1.8) + 32
		tempdif2 = stemp - float(ftemp2)
		print("\nEmergency Heat mode activated, current temperature is: " + str(ftemp2) + " Fahrenheit")
		print("set point is " + str(stemp))
		time.sleep(10)
		if tempdif2 > 0 :
			print("System Aux Heating")
			GPIO.output(G, True) 
			GPIO.output(W, True)

		elif tempdif2 <= 0 :
			print("temperature setpoint met")
			GPIO.output(G, False)
			GPIO.output(W, False)
			GPIO.output(Y, False)
			GPIO.output(O, False)

Gcounter = 0
def pin16_handler(pin) :

	if Gcounter == 0 :
		GPIO.output(G, True)
		Gcounter += 1
	else :
		Gcounter = 0
		GPIO.output(G, False)


GPIO.add_event_detect(24, GPIO.BOTH, pin24_handler)
GPIO.add_event_detect(23, GPIO.BOTH, pin23_handler)
GPIO.add_event_detect(13, GPIO.BOTH, pin13_handler)
GPIO.add_event_detect(16, GPIO.BOTH, pin16_handler)


try :

	print("Welcome to mythermostat")
	print("Current temperatre is: " + str(ftemp) + " Fahrenheit")
	#print("Current humidity is: " + str(hum))
	stemp = int(input("What temp would you like it to be? "))
	print("Please Enter Mode Selection ")
	pressenter = input("Use buttons to select HVAC mode, press enter to esc.")

except KeyboardInterrupt:
	GPIO.cleanup()

GPIO.output(G,False)
GPIO.output(Y,False)
GPIO.output(O, False)
GPIO.output(W, False)



GPIO.cleanup()
