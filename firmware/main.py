# UNTESTED, PROBABLY COULD BE BETTER BUT I CAN'T CHECK
# my favorite ide is notepad.exe (i don't wanna make a separate project folder for this)

import board
import busio
import time

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.macros import Macros

from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306

# I have no idea how most of this works. I'm mostly going off the tutorial and README.
# ULTRA UNORGANIZED

keyboard = KMKKeyboard()
encoder_handler = EncoderHandler()
macros = Macros()
# i feel like this could be better but i'm too scared to check
keyboard.modules.append(encoder_handler)
keyboard.modules.append(macros)
keyboard.modules.append(MediaKeys())

encoder_handler.pins = ((board.D6, board.D7, None))

# in order: d,f,j,k, prev track, pause, next track.

pins_used = [board.D0, board.D1, board.D2, board.D3, board.D10, board.D9, board.D8]

keyboard.matrix = KeysScanner(
	pins = pins_used,
	value_when_pressed = False,
)

# key commands, kps counter
# making a separate function for the macros wouldn't change much

key_press_counter = 0

# untested, could be optimized

def count():
	key_press_counter += 1

# could be better
keyboard.keymap = [[KC.MACRO(KC.D, count()), KC.MACRO(KC.F, count()), KC.MACRO(KC.J, count()), KC.MACRO(KC.K, count()), KC.MPRV, KC.MPLY, KC.MNXT]]
encoder_handler.map = [ ((KC.VOLD, KC.VOLU, KC.NO)) ]

# screen things

i2c_bus = busio.I2C(board.SCL, board.SDA)
driver =  SSD1306(i2c = i2c_bus)

screen = Display(
	display = driver,
	width = 128, 
	height = 32
)

keyboard.extensions.append(screen)

# i'll add bad apple later sometime once i get it
# 15fps 30*15 bad apple should fit

RECALC_DELAY = 0.5

def update():
	global key_press_counter
	display.clear()

	keys_per_second = key_press_counter / RECALC_DELAY

	display.entries = [TextEntry(text=f"KPS: {keys_per_second}", x=0, y=0)]

	key_press_counter = 0
	display.update()
	

# it's not like this will be imported
keyboard.go()
while True:
	update()
	time.sleep(RECALC_DELAY)
