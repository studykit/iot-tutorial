from machine import Pin, I2C
from writer import Writer
import korean_16 as fonts
from ssd1306 import SSD1306_I2C as SSD1306

# OLED display configuration (I2C)
_i2c = I2C(scl=Pin(12), sda=Pin(14))
_display = SSD1306(128, 64, _i2c)
_display.fill(0)

_writer = Writer(_display, fonts, False)
_writer.set_clip(True, True, False)

def clear():
    _display.fill(0)

def show():
    _display.show()

def print(string):
    _writer.printstring(string)

def set_textpos(row, col):
    Writer.set_textpos(_display, row, col)
