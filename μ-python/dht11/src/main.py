import display
import sensor
import time
import clock

clock.setup()
display.clear()

tick = True
while True:
    h, m, am_pm = clock.now()
    display.set_textpos(0, 0)

    if tick:
        # Read temperature and humidity from the sensor
        temperature, humidity = sensor.read()
        display.print(f"{am_pm} {h:02d}:{m:02d}\n")
        display.print(f"온도   {temperature}°\n")
        display.print(f"습도   {humidity}%\n")
    else:
        display.print(f"{am_pm} {h:02d} {m:02d}\n")

    tick = not tick

    # Update the display
    display.show()

    # Wait for 1 second
    time.sleep(1)
