import Adafruit_DHT
import time
import threading
import sys
import os
import RPi.GPIO as GPIO
from tkinter import *
from math import floor

# ====================== CONFIG ======================
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# Exact pins from your original code
RELAY_W = 12
RELAY_G = 18
RELAY_O = 20
RELAY_Y = 25

BTN_OFF_FAN = 16
BTN_HEAT = 24
BTN_COOL = 23
BTN_EMHEAT = 13

# Globals
stemp = 72
current_temp_f = 70
hvac_mode = "OFF"
fan_manual = False
running = True

# ====================== GPIO SETUP ======================
GPIO.setmode(GPIO.BCM)
GPIO.setup([RELAY_W, RELAY_G, RELAY_O, RELAY_Y], GPIO.OUT)
GPIO.output([RELAY_W, RELAY_G, RELAY_O, RELAY_Y], False)

for pin in [BTN_OFF_FAN, BTN_HEAT, BTN_COOL, BTN_EMHEAT]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ====================== GUI ======================
root = Tk()
root.title("CKTEMP18")
root.configure(bg="#0a0a0a")
root.attributes('-fullscreen', True)   # Perfect for small touchscreen

# Big fonts for small screen
title_font = ("Helvetica", 28, "bold")
big_temp_font = ("Helvetica", 72, "bold")
status_font = ("Helvetica", 18)

# Main container
main_frame = Frame(root, bg="#0a0a0a")
main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Current Temperature (HUGE)
temp_label = Label(main_frame, text="70°F", font=big_temp_font, fg="#00ffcc", bg="#0a0a0a")
temp_label.pack(pady=10)

setpoint_frame = Frame(main_frame, bg="#0a0a0a")
setpoint_frame.pack(pady=5)

Label(setpoint_frame, text="SETPOINT", font=("Helvetica", 14), fg="#888888", bg="#0a0a0a").pack()
sp_label = Label(setpoint_frame, text="72°F", font=("Helvetica", 48, "bold"), fg="white", bg="#0a0a0a")
sp_label.pack()

# Mode Status
mode_label = Label(main_frame, text="OFF", font=title_font, fg="#ff4444", bg="#0a0a0a")
mode_label.pack(pady=10)

# Status box
status_text = Text(main_frame, height=6, width=40, bg="#1a1a1a", fg="#00ffcc", font=("Helvetica", 14))
status_text.pack(pady=15, fill=X)

# Big control buttons
btn_frame = Frame(main_frame, bg="#0a0a0a")
btn_frame.pack(pady=20)

def create_mode_btn(text, color, row, col, mode):
    btn = Button(btn_frame, text=text, font=("Helvetica", 18, "bold"), bg=color, fg="white",
                 width=12, height=2, relief="flat", activebackground="#444444",
                 command=lambda: set_mode(mode))
    btn.grid(row=row, column=col, padx=8, pady=8)

create_mode_btn("HEAT", "#ff4444", 0, 0, "HEAT")
create_mode_btn("COOL", "#4488ff", 0, 1, "COOL")
create_mode_btn("EM HEAT", "#ff8800", 1, 0, "EMHEAT")
create_mode_btn("FAN ONLY", "#44ff88", 1, 1, "FAN")
Button(btn_frame, text="OFF", font=("Helvetica", 18, "bold"), bg="#555555", fg="white",
       width=12, height=2, relief="flat", command=lambda: set_mode("OFF")).grid(row=2, column=0, columnspan=2, pady=8)

# Setpoint +/- 
sp_btn_frame = Frame(main_frame, bg="#0a0a0a")
sp_btn_frame.pack(pady=10)

Button(sp_btn_frame, text="–", font=("Helvetica", 32), bg="#333333", fg="white", width=4, height=2,
       command=lambda: change_setpoint(-1)).grid(row=0, column=0, padx=20)
Button(sp_btn_frame, text="+", font=("Helvetica", 32), bg="#333333", fg="white", width=4, height=2,
       command=lambda: change_setpoint(1)).grid(row=0, column=1, padx=20)

# Bottom bar
bottom_frame = Frame(main_frame, bg="#0a0a0a")
bottom_frame.pack(side=BOTTOM, fill=X, pady=20)

Button(bottom_frame, text="QUIT TO TERMINAL", font=("Helvetica", 16, "bold"), bg="#ff2222", fg="white",
       command=quit_program, height=2).pack(side=RIGHT, padx=20)

# ====================== FUNCTIONS ======================
def update_gui():
    temp_label.config(text=f"{current_temp_f}°F")
    sp_label.config(text=f"{stemp}°F")
    
    colors = {"HEAT": "#ff4444", "COOL": "#4488ff", "EMHEAT": "#ff8800", "FAN": "#44ff88", "OFF": "#888888"}
    mode_label.config(text=hvac_mode, fg=colors.get(hvac_mode, "#888888"))
    
    status = f"Room: {current_temp_f}°F | Setpoint: {stemp}°F\n"
    status += f"Mode: {hvac_mode} | Fan: {'ON' if (hvac_mode=='FAN' or fan_manual) else 'AUTO'}\n"
    status_text.delete(1.0, END)
    status_text.insert(END, status)

def change_setpoint(delta):
    global stemp
    stemp = max(50, min(85, stemp + delta))
    update_gui()

def set_mode(new_mode):
    global hvac_mode, fan_manual
    hvac_mode = new_mode
    if new_mode == "FAN":
        fan_manual = True
    update_gui()

def read_sensor():
    global current_temp_f
    _, temp_c = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if temp_c is not None:
        current_temp_f = floor(temp_c * 1.8 + 32)

def control_loop():
    global hvac_mode
    while running:
        read_sensor()
        update_gui()
        
        diff = stemp - current_temp_f
        
        # Relay logic (exact same pins as your original)
        if hvac_mode == "HEAT":
            GPIO.output(RELAY_G, True)
            GPIO.output(RELAY_Y, diff > 0)
            GPIO.output(RELAY_W, False)
            GPIO.output(RELAY_O, False)
        elif hvac_mode == "COOL":
            GPIO.output(RELAY_G, True)
            GPIO.output(RELAY_Y, diff < 0)
            GPIO.output(RELAY_O, diff < 0)
            GPIO.output(RELAY_W, False)
        elif hvac_mode == "EMHEAT":
            GPIO.output(RELAY_G, True)
            GPIO.output(RELAY_W, diff > 0)
            GPIO.output(RELAY_Y, False)
            GPIO.output(RELAY_O, False)
        elif hvac_mode == "FAN":
            GPIO.output(RELAY_G, True)
            GPIO.output(RELAY_Y, False)
            GPIO.output(RELAY_W, False)
            GPIO.output(RELAY_O, False)
        else:  # OFF
            GPIO.output([RELAY_G, RELAY_Y, RELAY_W, RELAY_O], False)
        
        time.sleep(4)

def physical_button_handler(channel):
    global hvac_mode, fan_manual
    time.sleep(0.1)  # debounce
    if channel == BTN_HEAT:
        set_mode("HEAT")
    elif channel == BTN_COOL:
        set_mode("COOL")
    elif channel == BTN_EMHEAT:
        set_mode("EMHEAT")
    elif channel == BTN_OFF_FAN:
        if hvac_mode == "FAN":
            set_mode("OFF")
        else:
            set_mode("FAN")

# Attach physical buttons
for pin in [BTN_OFF_FAN, BTN_HEAT, BTN_COOL, BTN_EMHEAT]:
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=physical_button_handler, bouncetime=300)

def quit_program():
    global running
    running = False
    GPIO.cleanup()
    root.quit()
    sys.exit(0)

# ====================== START ======================
update_gui()

control_thread = threading.Thread(target=control_loop, daemon=True)
control_thread.start()

root.protocol("WM_DELETE_WINDOW", quit_program)
root.mainloop()