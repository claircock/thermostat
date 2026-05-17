import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import threading
import sys
import os
from tkinter import *
from math import floor

# ========================= CONFIG =========================
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# GPIO Pins
RELAY_W = 12   # White - Aux Heat
RELAY_G = 18   # Green - Fan
RELAY_O = 20   # Orange - Reversing Valve (Cool)
RELAY_Y = 25   # Yellow - Compressor

BUTTON_OFF = 16
BUTTON_HEAT = 24
BUTTON_COOL = 23
BUTTON_EMHEAT = 13

# Global variables
stemp = 70          # Default setpoint
current_temp_f = 70
hvac_mode = "OFF"   # OFF, HEAT, COOL, EMHEAT, FAN
fan_manual = False
running = True
# =======================================================

root = Tk()
root.title("CKTEMP18 - Pi Thermostat")

# ====================== GUI SETUP ======================
e = Entry(root, width=35, borderwidth=5, font=("Arial", 14), justify="center")
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
e.insert(0, "Press CLEAR then enter new setpoint")

thermostat_text = Text(root, width=45, height=10, font=("Helvetica", 12))
thermostat_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

def update_display():
    global current_temp_f, stemp, hvac_mode
    status = f"Mode: {hvac_mode}\n"
    status += f"Room Temp: {current_temp_f}°F\n"
    status += f"Setpoint: {stemp}°F\n"
    status += f"Fan: {'ON' if fan_manual else 'Auto'}"
    
    thermostat_text.delete(1.0, END)
    thermostat_text.insert(END, status)

# Button functions
def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(number))

def button_clear():
    e.delete(0, END)

def temp_ent():
    global stemp
    try:
        stemp = int(e.get())
        e.delete(0, END)
        e.insert(0, f"Setpoint updated to {stemp}°F")
        update_display()
    except:
        e.delete(0, END)
        e.insert(0, "Invalid number!")

def temp_up():
    global stemp
    stemp += 1
    update_display()

def temp_down():
    global stemp
    stemp -= 1
    update_display()

# Create all the buttons (same layout as yours)
buttons = [
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2),
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2),
    ("0", 4, 0)
]

for (text, row, col) in buttons:
    Button(root, text=text, padx=40, pady=20, 
           command=lambda t=text: button_click(t)).grid(row=row, column=col)

Button(root, text="Enter", bg="green", padx=28, pady=20, command=temp_ent).grid(row=4, column=2)
Button(root, text="Clear", padx=28, pady=20, command=button_clear).grid(row=4, column=1)
Button(root, text="+", padx=28, pady=20, command=temp_up).grid(row=5, column=2)
Button(root, text="-", padx=28, pady=20, command=temp_down).grid(row=5, column=1)
Button(root, text="Restart\nSystem", padx=17, pady=20, command=lambda: os.execl(sys.executable, sys.executable, *sys.argv)).grid(row=5, column=0)

# ====================== SENSOR READING ======================
def read_temperature():
    global current_temp_f
    humidity, temp_c = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if temp_c is not None:
        current_temp_f = floor(float(temp_c) * 1.8 + 32)
        return True
    return False

# ====================== HVAC CONTROL LOGIC ======================
def hvac_control_loop():
    global hvac_mode, current_temp_f, fan_manual
    
    while running:
        if not read_temperature():
            thermostat_text.insert(END, "\nSensor error...")
        
        update_display()
        
        temp_diff = stemp - current_temp_f
        
        # Main control logic
        if hvac_mode == "HEAT":
            if temp_diff > 0:
                GPIO.output(RELAY_G, True)   # Fan
                GPIO.output(RELAY_Y, True)   # Compressor
            else:
                GPIO.output(RELAY_G, False)
                GPIO.output(RELAY_Y, False)
                
        elif hvac_mode == "COOL":
            if temp_diff < 0:
                GPIO.output(RELAY_G, True)
                GPIO.output(RELAY_Y, True)
                GPIO.output(RELAY_O, True)   # Reversing valve
            else:
                GPIO.output(RELAY_G, False)
                GPIO.output(RELAY_Y, False)
                GPIO.output(RELAY_O, False)
                
        elif hvac_mode == "EMHEAT":
            if temp_diff > 0:
                GPIO.output(RELAY_G, True)
                GPIO.output(RELAY_W, True)   # Aux heat
            else:
                GPIO.output(RELAY_G, False)
                GPIO.output(RELAY_W, False)
                
        elif hvac_mode == "FAN":
            GPIO.output(RELAY_G, True)
        else:  # OFF
            GPIO.output(RELAY_G, False)
            GPIO.output(RELAY_Y, False)
            GPIO.output(RELAY_W, False)
            GPIO.output(RELAY_O, False)
        
        time.sleep(5)   # Check every 5 seconds

# ====================== PHYSICAL BUTTON HANDLERS ======================
def button_handler(channel):
    global hvac_mode, fan_manual
    
    time.sleep(0.05)  # debounce
    
    if channel == BUTTON_HEAT:
        hvac_mode = "HEAT"
        print("Heat mode activated")
    elif channel == BUTTON_COOL:
        hvac_mode = "COOL"
        print("Cool mode activated")
    elif channel == BUTTON_EMHEAT:
        hvac_mode = "EMHEAT"
        print("Emergency Heat activated")
    elif channel == BUTTON_OFF:
        hvac_mode = "OFF"
        print("System OFF")
    elif channel == BUTTON_FAN:   # I'll assume you have a fan button too
        fan_manual = not fan_manual
        if fan_manual:
            hvac_mode = "FAN"
        else:
            hvac_mode = "OFF"
    
    update_display()

# ====================== GPIO SETUP ======================
GPIO.setmode(GPIO.BCM)
GPIO.setup([RELAY_W, RELAY_G, RELAY_O, RELAY_Y], GPIO.OUT)
GPIO.output([RELAY_W, RELAY_G, RELAY_O, RELAY_Y], False)

for pin in [BUTTON_OFF, BUTTON_HEAT, BUTTON_COOL, BUTTON_EMHEAT]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_handler, bouncetime=300)

# ====================== START THREADS ======================
control_thread = threading.Thread(target=hvac_control_loop, daemon=True)
control_thread.start()

update_display()        # Show initial status
root.mainloop()         # This keeps the GUI running

# Cleanup when window is closed
running = False
GPIO.cleanup()