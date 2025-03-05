# Hardware Specifications

- **ESP8266**
  - Flash Memory: 4 MB
- **OLED Display (0.96", SSD1306) over I2C**
  - SCL: GPIO 12
  - SDA: GPIO 14
  - Resolution: 128 × 64 pixels
- **DHT11 Humidity and Temperature Sensor**
  - Connected via GPIO 16

# Runing main.py
## Installing MicroPython

```sh
pip3 install esptool
esptool --port /dev/ttyUSB0 erase_flash
esptool --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 "firmware"
```

Firmware can be downloaded from https://micropython.org/download/ESP8266_GENERIC/

For detailed instructions, refer to the [Getting Started with MicroPython on the ESP8266](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html#intro).

## Accessing the REPL
```sh
screen /dev/ttyUSB0 115200
```

## Connecting to WIFI
Network connectivity is essential as the system requires access to an NTP server for configuring the Real Time Clock (RTC).
Run the following code in the REPL:

```python
import network

#  Disable unused AP mode
ap = network.WLAN(network.WLAN.IF_AP)
ap.active(False)

wlan = network.WLAN(network.WLAN.IF_STA)
wlan.active(True)
wlan.connect('ssid', 'key')

# Wait until connected
import time

while not wlan.isconnected():
    print("Waiting for WIFI connection...")
    time.sleep(1)

wlan.config('addr4') # Check IP address

```

## Font Generation
Generate fonts with the following command:
```sh
./font_to_py.py d2-korean.ttf 16 korean_16.py -f -k charsets/korean
```
- **D2 Coding Font:** Download it from [GitHub](https://github.com/naver/d2codingfont).
- **font_to_py.py:** Download it from [GitHub](https://github.com/peterhinch/micropython-font-to-py).

## Copy Files to ESP8266 using the mpremote Command
```sh
for i in $(echo *.py)
do
  mpremote cp $i :.
done
```

For instructions on how to use `mpremote`, refer to [the documentation](https://docs.micropython.org/en/latest/reference/mpremote.html).

# References

## Core
- [ESP8266EX Datasheet](https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_en.pdf)

## Display
- [SSD1306 Datasheet](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf)
- [SSD1306 Driver](https://docs.micropython.org/en/latest/esp8266/quickref.html#ssd1306-driver)
- [I2C Driver](https://docs.micropython.org/en/latest/esp8266/quickref.html#i2c-bus)
- [writer.py](https://github.com/peterhinch/micropython-font-to-py/blob/master/writer/writer.py)


## DHT11
- [Basics of Interfacing DHT11/DHT22 Humidity and Temperature Sensor with MCU](https://www.ocfreaks.com/basics-interfacing-dht11-dht22-humidity-temperature-sensor-mcu/#:~:text=DHT11%20Data%20Format,3rd%20Byte+%204th%20Byte%7D)
- [DHT11 Datasheet](https://www.mouser.com/datasheet/2/758/DHT11-Technical-Data-Sheet-Translated-Version-1143054.pdf?srsltid=AfmBOopLiz_uh8k99vhOvKD9azUnptIdl67gPRFAkFOY7Rv2Q8cBL0Cb)
- [DHT Driver](https://docs.micropython.org/en/latest/esp8266/quickref.html#dht-driver)

