import time
import ntptime
from machine import RTC

clock_initialized = False
clock = RTC()

_pm = const("오후") # type: ignore
_am = const("오전") # type: ignore

def setup():
    global clock_initialized
    global clock

    if clock_initialized:
        return

    ntptime.host = 'time.google.com'
    ntptime.settime()  # Set the RTC to UTC time using ntptime

    # Get the current UTC time in seconds, add 9 hours (9*3600 seconds), and convert it to Korean time.
    utc_seconds = time.mktime(time.localtime())
    kst_seconds = utc_seconds + (9 * 3600)
    t = time.localtime(kst_seconds)

    clock.datetime((t[0], t[1], t[2], 0, t[3], t[4], t[5], 0))
    clock_initialized = True

def now():
    _, _, _, _, h, m, s, _ = clock.datetime()
    if h > 12:
        h -= 12
        return h, m, _pm
    else:
        return h, m, _am
