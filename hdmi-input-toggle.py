#!/usr/bin/python3
from evdev import InputDevice, ecodes
import subprocess
import re
import time

DEVICE_PATH = '/dev/input/event2'  # Update if needed
KEYCODE = 191  # Mapped to your button (e.g., F13)

def get_current_input():
    try:
        result = subprocess.run(
            ['ddcutil', 'getvcp', '0x60'],
            capture_output=True,
            text=True,
            check=True
        )
        match = re.search(r'sl=0x([0-9a-fA-F]+)', result.stdout)
        if match:
            current_hex = match.group(1).lower()
            print(f"Current input source is: 0x{current_hex}")
            return current_hex
        else:
            print("Failed to parse input source from ddcutil output.")
            return None
    except subprocess.CalledProcessError as e:
        print("Failed to run ddcutil:", e)
        return None

def set_input_source(new_hex):
    print(f"Switching input source to: {new_hex}")
    try:
        subprocess.run(['ddcutil', 'setvcp', '0x60', new_hex], check=True)
        subprocess.run(['ddcutil', 'setvcp', '0xdc', '00'], check=True)
    except subprocess.CalledProcessError as e:
        print("Failed to set input source:", e)

def toggle_input():
    current = get_current_input()
    if current is None:
        return
    if current == '03':
        new_hex = '17'
    elif current == '17':
        new_hex = '03'
    else:
        print(f"Unexpected input source: 0x{current}. Defaulting to 0x03.")
        new_hex = '03'
    set_input_source(new_hex)

# Start listening
dev = InputDevice(DEVICE_PATH)
print(f"Listening for keycode {KEYCODE} on {DEVICE_PATH}")

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.code == KEYCODE and event.value in (1, 2):  # press or hold
            toggle_input()
            time.sleep(1)  # crude debounce

