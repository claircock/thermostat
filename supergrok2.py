import Adafruit_DHT
import time
import threading
import sys
import RPi.GPIO as GPIO
from tkinter import *
from math import floor

# ====================== CONFIG ======================
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# Your exact original pins
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
running = True

# ====================== GPIO SETUP ======================
GPIO.setmode(GPIO.BCM)
GPIO.setup([RELAY_W, RELAY_G, RELAY_O, RELAY_Y], GPIO.OUT)
GPIO.output([RELAY_W, RELAY_G, RELAY_O, RELAY_Y], False)

for pin in [BTN_OFF_FAN, BTN_HEAT, BTN_COOL, BTN_EMHEAT]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ====================== GUI - SMALL SCREEN FRIENDLY ======================
root = Tk()
root.title("CKTEMP18")
root.configure(bg="#0a0a0a")
root.attributes('-fullscreen', True)  # Fullscreen for small touch

# Fonts tuned for 3" screen
big_temp_font = ("Helvetica", 52, "bold")
medium_font = ("Helvetica", 28, "bold")
small_font = ("Helvetica", 16)

main_frame = Frame(root, bg="#0a0a0a")
main_frame.pack(fill=BOTH, expand=True, padx=15, pady=10)

# Current Temperature
Label(main_frame, text="ROOM TEMP", font=small_font, fg="#888888", bg="#0a0a0a").pack()
temp_label = Label(main_frame, text="70°F", font=big_temp_font, fg="#00ffcc", bg="#0a0a0a")
temp_label.pack(pady=5)

# Setpoint
sp_frame = Frame(main_frame, bg="#0a0a0a")
sp_frame.pack(pady=8)
Label(sp_frame, text="SETPOINT", font=small_font, fg="#888888", bg="#0a0a0a").pack(side=LEFT)
sp_label = Label(sp_frame, text="72°F", font=medium_font, fg="white", bg="#0a0a0a")
sp_label.pack(side=LEFT, padx=15)

# Current Mode
mode_label = Label(main_frame, text="OFF", font=medium_font, fg="#ff4444", bg="#0a0a0a")
mode_label.pack(pady=10)

# Status Box
status_text = Text(main_frame, height=4, bg="#1a1a1a", fg="#00ff88", font=("Helvetica", 13))
status_text.pack(fill=X, pady=10)

# Mode Buttons
btn_frame = Frame(main_frame, bg="#0a0a0a")
btn_frame.pack(pady=15)

def make_mode_button(text, color, mode, row, col):
    btn = Button(btn_frame, text=text, font=("Helvetica", 14, "bold"), bg=color, fg="white",
                 width=10, height=2, relief="flat", activebackground="#333333",
                 command=lambda: set_mode(mode))
    btn.grid(row=row, column=col, padx=6, pady=6)
    return btn

make_mode_button("HEAT", "#ff4444", "HEAT", 0, 0)
make_mode_button("COOL", "#4488ff", "COOL", 0, 1)
make_mode_button("EM HEAT", "#ff8800", "EMHEAT", 1, 0)
make_mode_button("FAN", "#44ff88", "FAN", 1, 1)

Button(btn_frame, text="OFF", font=("Helvetica", 14, "bold"), bg="#555555", fg="white",
       width=22, height=2, relief="flat", command=lambda: set_mode("OFF")).grid(row=2, column=0, columnspan=2, pady=8)

# Setpoint +/- Buttons
sp_btn_frame = Frame(main_frame, bg="#0a0a0a")
sp_btn_frame.pack(pady=10)

Button(sp_btn_frame, text="–", font=("Helvetica", 28), bg="#333333", fg="white", width=4,
       command=lambda: change_setpoint(-1)).grid(row=0, column=0, padx=20)
Button(sp_btn_frame, text="+", font=("Helvetica", 28), bg="#333333", fg="white", width=4,
       command=lambda: change_setpoint(1)).grid(row=0, column=1, padx=20)

# Quit Button
Button(main_frame, text="QUIT TO TERMINAL", font=("Helvetica", 14, "bold"), bg="#cc2222", fg="white",
       command=lambda: quit_program(), height=2).pack(side=BOTTOM, fill=X, pady=15)

# ====================== FUNCTIONS ======================
def update_gui():
    temp_label.config(text=f"{current_temp_f}°F")
    sp_label.config(text=f"{stemp}°F")
    
    colors = {"HEAT": "#ff4444", "COOL": "#4488ff", "EMHEAT": "#ff8800", "FAN": "#44ff88", "OFF": "#888888"}
    mode_label.config(text=hvac_mode, fg=colors.get(hvac_mode, "#888888"))
    
    status = f"Mode: {hvac_mode}\n"
    status += f"Room: {current_temp_f}°F | Set: {stemp}°F\n"
    status += f"Fan: {'ON' if (hvac_mode in ['FAN']) else 'AUTO'}"
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
        
        # Control logic using your exact pins
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
    time.sleep(0.1)  # debounce
    if channel == BTN_HEAT:
        set_mode("HEAT")
    elif channel == BTN_COOL:
        set_mode("COOL")
    elif channel == BTN_EMHEAT:
        set_mode("EMHEAT")
    elif channel == BTN_OFF_FAN:
        set_mode("FAN" if hvac_mode != "FAN" else "OFF")

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
