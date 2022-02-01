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

#assign GPIO's as outputs
GPIO.setup(W, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(O, GPIO.OUT)
GPIO.setup(Y, GPIO.OUT)



#using adafruitDHT code convert to a temp in C and F 
ctemp = '{0:0.1f}'.format(temperature)
ftemp = (float(ctemp)*1.8) + 32
#hum = '{1:0.1f}%'.format(humidity)  <--this is not working



#monitor temp function



#start
print("AUTO mode")
print("Current temperature is: " + str(ctemp) + " Celsius")
print("Current temperatre is: " + str(ftemp))
#Current humidity is: " + str(hum)) <---not working

stemp = int(input("What temp would you like it to be? "))
print("here is ctemp: " + ctemp)
tempdif = stemp - float(ctemp)

i = tempdif

if tempdif >= 2 :
	print("heating mode")
	GPIO.output(G, True) 
	GPIO.output(Y, True)
	while True :
		humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
		if tempdif > 0 : 
			print("current temperature: " + str('{0:0.1f}'.format(temperature)) + "Temp dif: " + str(tempdif))
		time.sleep(5)
	else : print("moving on")
	print("met temp moving on bitch")
elif tempdif <= -2 :
	print("cooling  mode")
	GPIO.output(G,True)
	GPIO.output(Y,True)
	GPIO.output(O, True)

	pressenter = input("system now waiting for next cycle, press enter")


GPIO.output(G,False)
GPIO.output(Y,False)
GPIO.output(O, False)



GPIO.cleanup()

