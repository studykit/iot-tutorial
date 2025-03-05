.PHONY: copy

# Copy files to ESP32
copy:
	mpremote cp src/main.py :main.py
	mpremote cp src/display.py :display.py
	mpremote cp src/writer.py :writer.py
	mpremote cp src/sensor.py :sensor.py
	mpremote cp src/clock.py :clock.py
	mpremote cp src/korean_16.py :korean_16.py
	@echo "All files have been copied to ESP32."

# Generate font
korean_16.py: charsets/korean
	./font_to_py.py d2-korean.ttf 16 src/korean_16.py -f -k charsets/korean
	@echo "Korean font has been generated."

all: korean_16.py copy