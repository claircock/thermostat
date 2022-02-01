import Adafruit_DHT
import time
import RPi.GPIO as GPIO
from math import *
import signal
import sys
import os
from tkinter import *


#enter this at the begining of code when working with tkinter
root = Tk()
root.title("Temperture Keypad")

# DEFINE ENTRY BOX
e = Entry(root, width=35, borderwidth=5)

# PUT ENTRY BOX ON SCREEN
# use columnspan=3 to have this entry field to span over 3 columns
e.insert(0, "enter new temp at anytime ")
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)



def button_click(number):
	current = e.get()
	e.delete(0, END)
	e.insert(0, str(current) + str(number))

#clear previous number
def button_clear():
	e.delete(0, END)
#	GPIO.setmode(GPIO.BCM)

#	GPIO.output(G,False)
#	GPIO.output(Y,False)
#	GPIO.output(O, False)
#	GPIO.output(W, False)

#
#	GPIO.cleanup()


def sys_restart():
#	first_number = e.get()
#	global f_num

#	f_num = int(first_number)
#	e.delete(0, END)
	os.execl(sys.executable, sys.executable, *sys.argv)



def temp_ent() : #button_enter - button updates stemp
	global stemp
	stemp = int(e.get())
	e.delete(0, END)
	e.insert(0, "New temp updated. please select mode")
#	os.execl(sys.executable, sys.executable, *sys.argv)

button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: button_click(1))
button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: button_click(2))
button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: button_click(3))
button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: button_click(4))
button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: button_click(5))
button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: button_click(6))
button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: button_click(7))
button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: button_click(8))
button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: button_click(9))
button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: button_click(0))
button_enter = Button(root, text="Enter", bg="green", padx=28, pady=20, command=temp_ent)
button_clear = Button(root, text="clear", padx=28, pady=20, command=button_clear)
sys_restart = Button(root, text="System \nrestart", padx=17, pady=20, command=sys_restart)

# put the buttons on the screen
button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)

button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)
button_0.grid(row=4, column=0)
button_enter.grid(row=4, column=2)
button_clear.grid(row=4, column=1)
sys_restart.grid(row=5,column=0)

#DHT11 setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

#my variable gpio pin assignments

#using adafruitDHT code convert to a temp in C and F 
ctemp = '{0:0.1f}'.format(temperature)
ftemp = floor(float(ctemp)*1.8) + 32
#hum = '{1:0.1f}%'.format(humidity)  

#Current humidity is: " + str(hum)) <---not working


def set_temp() :
	print("Welcome to mythermostat")
	print("Current temperatre is: " + str(ftemp) + " Fahrenheit")
#	pressenter = input("\nUse buttons to select HVAC mode, press enter to esc.")
#	global stemp
#	print("what temperature would you like? ")
#	stemp = int(e.get())



#global pin24_handler
def pin24_handler(pin):
	while True :
		try :
			DHT_SENSOR = Adafruit_DHT.DHT11
			DHT_PIN = 4
			humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
			ctemp2 = '{0:0.1f}'.format(temperature)
			ftemp2 = floor(float(ctemp2)*1.8) + 32
			tempdif2 = stemp - int(ftemp2)

			print("\nHeating mode activated, current temperature is: " + str(ftemp2) + " Fahrenheit")
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
				time.sleep(300)

		except :
			print("\nNo responce from DHT")
			pin24_handler
			time.sleep(5)
#global pin23_handler
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
				time.sleep(300)

		except :
			print("\nNo responce from DHT")
			pin24_handler
			time.sleep(5)
#global pin13_handler
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
				time.sleep(300)
		except :
			print("\nNo responce from DHT")
			pin24_handler
			time.sleep(5)


def pin16_handler(pin) :
	print("shits not working")

#while True :
GPIO.setmode(GPIO.BCM)
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


GPIO.add_event_detect(24, GPIO.BOTH, pin24_handler)
GPIO.add_event_detect(23, GPIO.BOTH, pin23_handler)
GPIO.add_event_detect(13, GPIO.BOTH, pin13_handler)
GPIO.add_event_detect(16, GPIO.BOTH, pin16_handler) 

print("sys start")
set_temp()
#stemp = int(input("What temp would you like it to be? "))


end_program = input("Plese select HVAC mode: \nRed - HP Heat Mode \nYellow - Em Heat Mode \nBlue - Cooling Mode \nPress enter anytime to end program")
GPIO.output(G,False)
GPIO.output(Y,False)
GPIO.output(O, False)
GPIO.output(W, False)


GPIO.cleanup()
os.execl(sys.executable, sys.executable, *sys.argv)
#root.mainloop()
