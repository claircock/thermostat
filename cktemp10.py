import Adafruit_DHT
import time
import RPi.GPIO as GPIO


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
ftemp = (float(ctemp)*1.8) + 32
#hum = '{1:0.1f}%'.format(humidity)  <--this is not working


#start


#Current humidity is: " + str(hum)) <---not working

def pin24_handler(pin):
	while True :
		DHT_SENSOR = Adafruit_DHT.DHT11
		DHT_PIN = 4
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		ctemp2 = '{0:0.1f}'.format(temperature)
		tempdif2 = stemp - float(ctemp2)
		print("\nHeating mode activated, current temperature is: " + str(ctemp2) + " celcius")
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

def pin23_handler(pin):
	while True :
		DHT_SENSOR = Adafruit_DHT.DHT11
		DHT_PIN = 4
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		ctemp2 = '{0:0.1f}'.format(temperature)
		tempdif2 = stemp - float(ctemp2)
		print("\nCooling mode activated, current temperature is: " + str(ctemp2) + " celcius")
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


def pin13_handler(pin) :
	while True :
		DHT_SENSOR = Adafruit_DHT.DHT11
		DHT_PIN = 4
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		ctemp2 = '{0:0.1f}'.format(temperature)
		tempdif2 = stemp - float(ctemp2)
		print("\nEmergency Heat mode activated, current temperature is: " + str(ctemp2) + " celcius")
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
GPIO.add_event_detect(24, GPIO.BOTH, pin24_handler)
GPIO.add_event_detect(23, GPIO.BOTH, pin23_handler)
GPIO.add_event_detect(13, GPIO.BOTH, pin13_handler)


try :

	print("Welcome to mythermostat")
	print("current temperature is: " + str(ctemp) + " celcius")
	print("Current temperatre is: " + str(ftemp) + "Fahrenheit")
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
