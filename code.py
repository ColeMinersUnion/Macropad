#Partially Derived from code available for free at learn.adafruit.com
#import statements, importing the necessary packages
import rotaryio #encoder
import board #interfacing with the microcontroller
import digitalio
import usb_hid
import random
import keypad
import time
import neopixel
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

#setup
#initializing all variables & objects
#setting the mute button
button = digitalio.DigitalInOut(board.GP17)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

#creating an encoder object
encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP15)

#setting up the keypoad and volume controls
cc = ConsumerControl(usb_hid.devices)

#using the encoder button as a toggle
button_state = None
last_position = encoder.position

#setting up the keys
#How bright the LEDs are
BRIGHTNESS = 0.5

#labelling board pins
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


#running loop of code.
#Runs continuously
while True:
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
        
        
    #This is my encoder code.
    #calc change of position
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
    
        

