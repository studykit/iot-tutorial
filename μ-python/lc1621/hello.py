from machine import Pin
import time

# Define GPIO pins (adjust these numbers as needed)
RS_PIN = 0   # Register Select pin
E_PIN  = 1   # Enable pin
D0_PIN = 2   # Data pin D0
D1_PIN = 3   # Data pin D1
D2_PIN = 4   # Data pin D2
D3_PIN = 5   # Data pin D3
D4_PIN = 6   # Data pin D4
D5_PIN = 7   # Data pin D5
D6_PIN = 8   # Data pin D6
D7_PIN = 9   # Data pin D7

# Initialize control pins
rs = Pin(RS_PIN, Pin.OUT)
e  = Pin(E_PIN, Pin.OUT)

# Initialize data pins D0 through D7
d0 = Pin(D0_PIN, Pin.OUT)
d1 = Pin(D1_PIN, Pin.OUT)
d2 = Pin(D2_PIN, Pin.OUT)
d3 = Pin(D3_PIN, Pin.OUT)
d4 = Pin(D4_PIN, Pin.OUT)
d5 = Pin(D5_PIN, Pin.OUT)
d6 = Pin(D6_PIN, Pin.OUT)
d7 = Pin(D7_PIN, Pin.OUT)

# Create a list for easier access
data_pins = [d0, d1, d2, d3, d4, d5, d6, d7]

def pulse_enable():
    e.value(1)
    time.sleep_us(1)    # Minimum pulse width (≥450 ns recommended)
    e.value(0)
    time.sleep_us(100)  # Delay for the LCD to process the command

def send_command(cmd):
    rs.value(0)  # RS low: command mode
    # Set data pins according to each bit in the command
    for i in range(8):
        # Extract the i-th bit (0 or 1)
        data_pins[i].value((cmd >> i) & 0x01)
    pulse_enable()


def send_data(data):
    rs.value(1)  # RS high for data mode
    # Set the data pins for each bit of the data byte
    for i in range(8):
        data_pins[i].value((data >> i) & 0x01)
    pulse_enable()

# Main initialization sequence
time.sleep_ms(40)  # Wait for 40ms after power-up for LCD stabilization

# 1. Function Set: 8-bit mode, 2 lines, 5x8 dot font (command 0x38)
send_command(0x38)
time.sleep_ms(5)

# 2. Display On/Off Control: Display ON, cursor OFF, blink OFF (command 0x0C)
send_command(0x0C)
time.sleep_ms(5)

# 3. Clear Display (command 0x01)
send_command(0x01)
time.sleep_ms(5)

# 4. Entry Mode Set: Increment mode, no display shift (command 0x06)
send_command(0x06)
time.sleep_ms(5)

# --- Write "Hello World" to the LCD ---
message = "Hello World"
for ch in message:
    send_data(ord(ch))

# At this point, the LCD is initialized in 8-bit mode.
# Your application code can now send data (using a similar routine but with RS set to 1).

while True:
    # Main loop - insert additional display routines here
    time.sleep_ms(1000)
    pass
