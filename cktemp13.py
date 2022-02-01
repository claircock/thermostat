import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from math import *
#import os
#import sys

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
OFF = 16
HEAT = 24
COOLING = 23
EMHEAT= 13

#assign GPIO's as outputs
GPIO.setup(W, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(O, GPIO.OUT)
GPIO.setup(Y, GPIO.OUT)
GPIO.setup(OFF,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(HEAT,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(COOLING,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(EMHEAT,GPIO.IN,pull_up_down=GPIO.PUD_UP)


#using adafruitDHT code convert to a temp in C and F 
ctemp = '{0:0.1f}'.format(temperature)
ftemp = floor(float(ctemp)*1.8) + 32
#hum = '{1:0.1f}%'.format(humidity)  


#start


#Current humidity is: " + str(hum)) <---not working

while True:

#	def set_temp() :

	#	print("Current humidity is: " + str(hum)
	#	print("Please Enter Mode Selection ")
	#	pressenter = input("\nUse buttons to select HVAC mode, press enter to esc.")
	
	GPIO.setmode(GPIO.BCM)


	def pin24_handler(pin):
		while True :
			#try :
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

			#except :
			#	print("\nNo responce from DHT")
			#	pin24_handler
			#	time.sleep(5)

	def pin23_handler(pin):
		while True :
			try :
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
					time.sleep(60)
			except :
				print("\nNo responce from DHT")
				pin23_handler
				time.sleep(5)



	def pin13_handler(pin) :
		while True :
			try :
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
					time.sleep(60)
			except :
				print("\nNo responce from DHT")
				pin13_handler
				time.sleep(5)

	def pin16_handler(pin) :
		print("fuck")



	GPIO.add_event_detect(24, GPIO.BOTH, pin24_handler)
	GPIO.add_event_detect(23, GPIO.BOTH, pin23_handler)
	GPIO.add_event_detect(13, GPIO.BOTH, pin13_handler)
	GPIO.add_event_detect(16, GPIO.BOTH, pin16_handler) 

	print("shits not working")
	print("sys start")
	print("Welcome to mythermostat")
	print("Current temperatre is: " + str(ftemp) + " Fahrenheit")
	stemp = int(input("What temp would you like it to be? "))
	end_program = input("Plese select HVAC mode: \nRed - HP Heat Mode \nYellow - Em Heat Mode \nBlue - Cooling Mode \nPress enter anytime to end program")



#	hitenter = input("press sstart to begin, press enter to esc.")




	GPIO.output(G,False)
	GPIO.output(Y,False)
	GPIO.output(O, False)
	GPIO.output(W, False)



	GPIO.cleanup()
