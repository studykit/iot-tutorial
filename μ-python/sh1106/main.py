from machine import I2C, Pin
from sh1106 import SH1106_I2C

i2c = I2C(0, scl=Pin(9), sda=Pin(8))

# Create an SH1106 instance for a 128x64 display.
display = SH1106_I2C(128, 64, i2c)

# Clear the display (fill with black)
display.fill(0)
display.text('Hellow', 0, 0, 1)
display.show()