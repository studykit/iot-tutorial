import spidev
import RPi.GPIO as GPIO
import time

# Define GPIO pins
DC_PIN = 25
RESET_PIN = 24


# Suppress warnings if the pins are already in use
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DC_PIN, GPIO.OUT)
GPIO.setup(RESET_PIN, GPIO.OUT)

# Initialize SPI (using CE0 on bus 0)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 40000000  # Adjust as needed
spi.mode = 0

# Display dimensions
WIDTH = 240
HEIGHT = 320

# Create a frame buffer (16 bits per pixel, so 2 bytes per pixel)
frame_buffer = bytearray(WIDTH * HEIGHT * 2)

def send_command(cmd):
    GPIO.output(DC_PIN, GPIO.LOW)  # Command mode
    spi.xfer([cmd])

def send_data(data):
    GPIO.output(DC_PIN, GPIO.HIGH)  # Data mode
    if isinstance(data, (list, bytearray)):
        spi.xfer2(data)
    else:
        spi.xfer([data])

def reset_display():
    GPIO.output(RESET_PIN, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(RESET_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    time.sleep(0.12)

def init_display():
    reset_display()
    send_command(0x01)  # Software Reset
    time.sleep(0.1)
    send_command(0x11)  # Sleep Out
    time.sleep(0.12)
    send_command(0x3A)  # Pixel Format Set
    send_data(0x55)     # 16-bit/pixel
    send_command(0x36)  # Memory Access Control
    send_data(0x48)     # Adjust for rotation/color order (modify as needed)
    send_command(0x29)  # Display ON
    time.sleep(0.1)

def set_addr_window(x0, y0, x1, y1):
    # Column Address Set
    send_command(0x2A)
    send_data(x0 >> 8)
    send_data(x0 & 0xFF)
    send_data(x1 >> 8)
    send_data(x1 & 0xFF)
    
    # Page Address Set
    send_command(0x2B)
    send_data(y0 >> 8)
    send_data(y0 & 0xFF)
    send_data(y1 >> 8)
    send_data(y1 & 0xFF)
    
    # Memory Write
    send_command(0x2C)

def clear_buffer(color):
    """Fill the frame buffer with the given 16-bit color."""
    hi = (color >> 8) & 0xFF
    lo = color & 0xFF
    for i in range(0, len(frame_buffer), 2):
        frame_buffer[i] = hi
        frame_buffer[i+1] = lo

def set_pixel(x, y, color):
    """Set a single pixel in the frame buffer with the given 16-bit color."""
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return
    index = (y * WIDTH + x) * 2
    frame_buffer[index] = (color >> 8) & 0xFF
    frame_buffer[index+1] = color & 0xFF

def draw_line(x0, y0, x1, y1, color):
    """Draw a line from (x0, y0) to (x1, y1) using Bresenham's algorithm."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy  # error value e_xy
    while True:
        set_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

def update_display():
    """Push the entire frame buffer to the display in chunks."""
    set_addr_window(0, 0, WIDTH - 1, HEIGHT - 1)
    chunk_size = 4096  # bytes per SPI transfer
    for i in range(0, len(frame_buffer), chunk_size):
        spi.xfer2(frame_buffer[i:i+chunk_size])

def main():
    try:
        init_display()
        # Clear screen to white so the black line is visible
        clear_buffer(0xFFFF)
        # Draw a black line from (20, 20) to (220, 300)
        draw_line(20, 20, 220, 300, 0xF800)
        # Update the display with the new frame buffer contents
        update_display()
        time.sleep(10)  # Display remains on for 10 seconds
    except KeyboardInterrupt:
        pass
    finally:
        spi.close()
        GPIO.cleanup()

if __name__ == '__main__':
    main()