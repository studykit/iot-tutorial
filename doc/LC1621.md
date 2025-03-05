# Overview

This project provides code to control the LC1621 LCD module using MicroPython. The LC1621 is a 16x2 character LCD that is controlled through an 8-bit parallel interface.

## Key Features
- 8-bit data mode support
- 16x2 character display (32 characters)
- 5x8 dot font
- Backlight support
- 3.3V or 5V logic level support

## Implemented Features
- LCD initialization sequence
- Command transmission
- Data transmission
- Enable pulse control
- Basic text output

## Core Components Used
- `machine.Pin`: GPIO pin control
- `time`: Timing control

## PIN Connection for 8Bit Mode

| LC1641 Pin No. | Signal/Function      | RP2040 Connection (Example)        | Comments                                                    |
| -------------- | -------------------- | ---------------------------------- | ----------------------------------------------------------- |
| 1              | VSS (GND)            | GND                                | Common ground                                               |
| 2              | VDD (Logic Supply)   | 3.3V (or regulated 5V* )           | Use 3.3V if logic-level shifting isn't required             |
| 3              | VO (Contrast Adjust) | Potentiometer wiper                | Potentiometer between VDD and GND for contrast control      |
| 4              | RS (Register Select) | GPIO 0                             | RS = 0 for command, RS = 1 for data                         |
| 5              | R/W (Read/Write)     | GND                                | Tie to GND for write‑only operation                         |
| 6              | E (Enable)           | GPIO 1                             | Enable pulses latch data on falling edge                    |
| 7              | DB0 (Data Bit 0)     | GPIO 2                             |                                                             |
| 8              | DB1 (Data Bit 1)     | GPIO 3                             |                                                             |
| 9              | DB2 (Data Bit 2)     | GPIO 4                             |                                                             |
| 10             | DB3 (Data Bit 3)     | GPIO 5                             |                                                             |
| 11             | DB4 (Data Bit 4)     | GPIO 6                             |                                                             |
| 12             | DB5 (Data Bit 5)     | GPIO 7                             |                                                             |
| 13             | DB6 (Data Bit 6)     | GPIO 8                             |                                                             |
| 14             | DB7 (Data Bit 7)     | GPIO 9                             |                                                             |
| 15             | LEDA (Backlight +)   | 5V (via current‑limiting resistor) | Use a resistor (e.g., 100–220Ω) for proper current limiting |
| 16             | LEDK (Backlight –)   | GND                                |                                                             |

## Initialization Sequence

![250](resources/8bit-initialization.png)
1. Function Set (0x38): 8-bit mode, 2 lines, 5x8 dot font
2. Display On/Off Control (0x0C): Display ON, cursor OFF, blink OFF
3. Clear Display (0x01): Screen initialization
4. Entry Mode Set (0x06): Increment mode, no display shift

# References

[LC1621-SMLYH6-DH3 Datasheet](https://www.icbanq.com/icdownload/V2_DATA/ICBShop/Board/202203/f260bb128a90438fb8112301257eaff6.pdf)
