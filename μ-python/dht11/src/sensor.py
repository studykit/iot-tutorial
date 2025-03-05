from machine import Pin
import dht

# DHT11 sensor configuration
_sensor = dht.DHT11(Pin(16))  # D0 pin corresponds to GPIO16

def read():
    _sensor.measure()
    temp = _sensor.temperature()
    hum = _sensor.humidity()
    return temp, hum
