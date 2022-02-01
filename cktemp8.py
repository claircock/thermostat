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
print("STANDBY mode")
print("Current temperature is: " + str(ctemp) + " Celsius")
print("Current temperatre is: " + str(ftemp) + "Fahrenheit")
#Current humidity is: " + str(hum)) <---not working

try:
	print("Please Enter Mode Selection ")

	GPIO.wait_for_edge(24, GPIO.FALLING)
	print("current temperature: " + str(ctemp))
	stemp = int(input("What temp would you like it to be? "))


	while True :
		DHT_SENSOR = Adafruit_DHT.DHT11
		DHT_PIN = 4
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		ctemp2 = '{0:0.1f}'.format(temperature)
		tempdif2 = stemp - float(ctemp2)


		time.sleep(5)
		if tempdif2 > 0 :
			print("System Heating")
			GPIO.output(G, True) 
			GPIO.output(Y, True)

		elif tempdif2 <= 0 :
			print("temperature setpoint met")
			GPIO.output(G, False)
			GPIO.output(Y, False)
			break

	GPIO.wait_for_edge(23, GPIO.FALLING)
	print("current temperature: " + str(ctemp))
	stemp = int(input("What temp would you like it to be? "))


	while True :

		DHT_SENSOR = Adafruit_DHT.DHT11
		DHT_PIN = 4
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		ctemp2 = '{0:0.1f}'.format(temperature)
		tempdif2 = stemp - float(ctemp2)

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
			break

	GPIO.wait_for_edge(16, GPIO.FALLING)
	print("sys EMheating shiiiiiiieeeit")
		
	time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()


else :
	print("somthings not working")

pressenter = input("system now waiting for next cycle, press enter")

GPIO.output(G,False)
GPIO.output(Y,False)
GPIO.output(O, False)



GPIO.cleanup()
