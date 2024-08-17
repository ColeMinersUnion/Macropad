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
