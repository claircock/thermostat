# ================================================
# CKTEMP18 - supergrok3.py
# Optimized for 1280x720 resolution
# ================================================

import Adafruit_DHT
import time
import threading
import os
import RPi.GPIO as GPIO
from tkinter import *
from math import floor

# ====================== CONFIG ======================
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

RELAY_W = 12
RELAY_G = 18
RELAY_O = 20
RELAY_Y = 25

BTN_OFF_FAN = 16
BTN_HEAT = 24
BTN_COOL = 23
BTN_EMHEAT = 13

stemp = 72
current_temp_f = 70
hvac_mode = "OFF"
running = True

# ====================== GPIO ======================
GPIO.setmode(GPIO.BCM)
GPIO.setup([RELAY_W, RELAY_G, RELAY_O, RELAY_Y], GPIO.OUT)
GPIO.output([RELAY_W, RELAY_G, RELAY_O, RELAY_Y], False)

for pin in [BTN_OFF_FAN, BTN_HEAT, BTN_COOL, BTN_EMHEAT]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ====================== GUI - 1280x720 OPTIMIZED ======================
root = Tk()
root.title("CKTEMP18")
root.configure(bg="#0a0a0a")
root.attributes('-fullscreen', True)

# Fonts tuned for 1280x720
big_font = ("Helvetica", 80, "bold")
med_font = ("Helvetica", 42, "bold")
small_font = ("Helvetica", 24)
btn_font = ("Helvetica", 18, "bold")

main = Frame(root, bg="#0a0a0a")
main.pack(fill=BOTH, expand=True, padx=30, pady=20)

# Left Side - Big Display
left = Frame(main, bg="#0a0a0a")
left.pack(side=LEFT, fill=Y, expand=True, padx=20)

Label(left, text="ROOM TEMP", font=small_font, fg="#888888", bg="#0a0a0a").pack(anchor="w")
temp_label = Label(left, text="70°F", font=big_font, fg="#00ffcc", bg="#0a0a0a")
temp_label.pack(pady=15, anchor="w")

sp_frame = Frame(left, bg="#0a0a0a")
sp_frame.pack(pady=15, anchor="w")
Label(sp_frame, text="SETPOINT", font=small_font, fg="#888888", bg="#0a0a0a").pack(side=LEFT)
sp_label = Label(sp_frame, text="72°F", font=med_font, fg="white", bg="#0a0a0a")
sp_label.pack(side=LEFT, padx=25)

mode_label = Label(left, text="OFF", font=med_font, fg="#ff4444", bg="#0a0a0a")
mode_label.pack(pady=20, anchor="w")

status_text = Text(left, height=6, bg="#1a1a1a", fg="#00ff88", font=("Helvetica", 17), width=35)
status_text.pack(pady=15, anchor="w")

# Right Side - Controls
right = Frame(main, bg="#0a0a0a")
right.pack(side=RIGHT, fill=Y, padx=20)

# Mode buttons
btn_frame = Frame(right, bg="#0a0a0a")
btn_frame.pack(pady=10)

def make_btn(text, color, mode, r, c):
    Button(btn_frame, text=text, font=btn_font, bg=color, fg="white", width=12, height=2,
           command=lambda: set_mode(mode)).grid(row=r, column=c, padx=10, pady=8)

make_btn("HEAT", "#ff4444", "HEAT", 0, 0)
make_btn("COOL", "#4488ff", "COOL", 0, 1)
make_btn("EM HEAT", "#ff8800", "EMHEAT", 1, 0)
make_btn("FAN", "#44ff88", "FAN", 1, 1)

Button(btn_frame, text="OFF", font=btn_font, bg="#555555", fg="white", width=27, height=2,
       command=lambda: set_mode("OFF")).grid(row=2, column=0, columnspan=2, pady=12)

# Setpoint +/- 
sp_btn_frame = Frame(right, bg="#0a0a0a")
sp_btn_frame.pack(pady=20)
Button(sp_btn_frame, text="–", font=("Helvetica", 48), bg="#333333", fg="white", width=3,
       command=lambda: change_setpoint(-1)).grid(row=0, column=0, padx=25)
Button(sp_btn_frame, text="+", font=("Helvetica", 48), bg="#333333", fg="white", width=3,
       command=lambda: change_setpoint(1)).grid(row=0, column=1, padx=25)

# Bottom Control Buttons (Guaranteed visible)
bottom = Frame(right, bg="#0a0a0a")
bottom.pack(side=BOTTOM, fill=X, pady=30)

Button(bottom, text="EXIT TO DESKTOP", font=btn_font, bg="#ff8800", fg="white", height=2,
       command=lambda: exit_to_desktop()).pack(side=LEFT, fill=X, expand=True, padx=12)

Button(bottom, text="⏻ SHUTDOWN PI", font=btn_font, bg="#cc2222", fg="white", height=2,
       command=lambda: safe_shutdown()).pack(side=RIGHT, fill=X, expand=True, padx=12)

# ====================== FUNCTIONS ======================
def update_gui():
    temp_label.config(text=f"{current_temp_f}°F")
    sp_label.config(text=f"{stemp}°F")
    colors = {"HEAT":"#ff4444","COOL":"#4488ff","EMHEAT":"#ff8800","FAN":"#44ff88","OFF":"#888888"}
    mode_label.config(text=hvac_mode, fg=colors.get(hvac_mode,"#888888"))
    
    status = f"Mode: {hvac_mode}\nRoom: {current_temp_f}°F\nSetpoint: {stemp}°F"
    status_text.delete(1.0, END)
    status_text.insert(END, status)

def change_setpoint(delta):
    global stemp
    stemp = max(50, min(85, stemp + delta))
    update_gui()

def set_mode(new_mode):
    global hvac_mode
    hvac_mode = new_mode
    update_gui()

def read_sensor():
    global current_temp_f
    _, temp_c = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if temp_c is not None:
        current_temp_f = floor(temp_c * 1.8 + 32)

def control_loop():
    while running:
        read_sensor()
        update_gui()
        diff = stemp - current_temp_f
        
        if hvac_mode == "HEAT":
            GPIO.output(RELAY_G, True)
            GPIO.output(RELAY_Y, diff > 0)
        elif hvac_mode == "COOL":
            GPIO.output(RELAY_G, True)
            GPIO.output(RELAY_Y, diff < 0)
            GPIO.output(RELAY_O, diff < 0)
        elif hvac_mode == "EMHEAT":
            GPIO.output(RELAY_G, True)
            GPIO.output(RELAY_W, diff > 0)
        elif hvac_mode == "FAN":
            GPIO.output(RELAY_G, True)
        else:
            GPIO.output([RELAY_G, RELAY_Y, RELAY_W, RELAY_O], False)
        time.sleep(4)

def physical_button_handler(channel):
    time.sleep(0.1)
    if channel == BTN_HEAT: set_mode("HEAT")
    elif channel == BTN_COOL: set_mode("COOL")
    elif channel == BTN_EMHEAT: set_mode("EMHEAT")
    elif channel == BTN_OFF_FAN:
        set_mode("FAN" if hvac_mode != "FAN" else "OFF")

def exit_to_desktop():
    global running
    running = False
    GPIO.cleanup()
    root.quit()

def safe_shutdown():
    global running
    running = False
    GPIO.cleanup()
    status_text.delete(1.0, END)
    status_text.insert(END, "Shutting down Pi...")
    root.update()
    os.system("sudo shutdown -h now")

# Physical button setup
for pin in [BTN_OFF_FAN, BTN_HEAT, BTN_COOL, BTN_EMHEAT]:
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=physical_button_handler, bouncetime=300)

# Start program
update_gui()
threading.Thread(target=control_loop, daemon=True).start()
root.mainloop()
