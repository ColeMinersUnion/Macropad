# My Macropad
## Description

This macropad was built with a Raspberry Ri Rico using [CircuitPython.](https://circuitpython.org/) The code in this repository includes volume control and a Three pseudo-Clipboards. Shown below are instructions as well as files to edit or order PCBs. 

## Setup
### Thonny
Please install the latest version of thonny available at: [Thonny](https://thonny.org/). Thonny is a code editor that specializes in developing solutions for CircuitPython and MicroPython systems. 

### Supporting Documentation
For more information on the Mechanical Key breakout boards, as well as some of the code used in development: [Adafruit Tutorial](https://learn.adafruit.com/neokey-breakout/circuitpython-python) \
For more information on the Rotary Encoder, specifically as a volume knob: [Adafruit Tutorial](https://learn.adafruit.com/trinket-usb-volume-knob/add-a-mute-button) \

## Shopping List

## Wiring
### Breadboard

### Printed Circuit Board

## Code
### Library Downloads
All of these libraries can be found on [pypi](https://pypi.org/)) for more information.\
Libraries To Download\
├── adafruit-circuitpython-neopixel\
└── adafruit-circuitpython-hid

### Import Statements
Import all of the necessary libraries. Most of which are included in the circuitpython interpreter.
```Python
#Basic Imports
import board
import time
import usb_hid

#For the Rotary Encoder
import digitalio
import rotaryio
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control import ConsumerControlCode

#For the keys
import keypad
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
```

### Setting up the Encoder
This sets up all of the neccessary objects and variables for the encoder functionality. We use a button state variable to track mute state. 
```Python
#setting the mute button
button = digitalio.DigitalInOut(board.GP17)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
#setting up the keypoad and volume controls
cc = ConsumerControl(usb_hid.devices
#using the encoder button as a toggle
button_state = None
last_position = encoder.position
```

### Setting up the Keys
This section is meant to be general and just to show how the keys work before implementing layers or extra functionality. It does follow the previous physical prototype, notably that there are only 5 keys. 
```Python
#setting the brightness
#Any value from 0-1, the LEDs are very bright
BRIGHTNESS = 0.25

PIXEL_PIN = board.GP28
KEY_PINS = (board.GP27, board.GP26, board.GP22, board.GP21, board.GP20)
KEY_VALUE = (Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.E)
NUM_PIXELS = len(KEY_PINS)

#creating the neopixel obj
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS)
#initial light up
for k in pixels:
    k = (0, 255, 0)

#creating a keypad obj
keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)
time.sleep(1) #avoiding conflicts with OS
kboard = Keyboard(usb_hid.devices)
```

### Running Loop (Encoder)
Both sections of code in Running Loop should be wrapped in the SAME loop:
```Python
while(true):
```
This section details how the encoder runs to mute, decrement, or increment volume. 
```Python
    #This is my encoder code.
    #calculate change of position
    current_position = encoder.position
    position_change = current_position - last_position
    #logic for encoder.
    if position_change > 0:
        for _ in range(position_change):
            #changing volume
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    last_position = current_position
    
    #muting. 
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button pressed.")
        cc.send(ConsumerControlCode.MUTE)
        button_state = None
```
### Running Loop (Keys)
Most of the heavy lifting for the keys was done during initialization. 
```Python
    #keyboard stuff
    event = keys.events.get()
    
    #initial push.
    if event and event.pressed:
        #which key did I press?
        key_index = event.key_number
        print(key_index)
        #on push
        pixels[key_index] = (0, 0, 255)
        kboard.press(KEY_VALUE[key_index])
        
    if event and event.released:
        pixels[event.key_number] =(0, 255, 0)
        kboard.release_all()
```

## Additional Features

