# DNS-mixer Makefile

.PHONY: help build clean flash install-deps

# Default target
help:
	@echo "DNS-mixer Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  build        - Build firmware for both ESP8266 and ESP32"
	@echo "  build-esp8266 - Build firmware for ESP8266 only"
	@echo "  build-esp32   - Build firmware for ESP32 only"
	@echo "  clean         - Clean build artifacts"
	@echo "  flash         - Flash firmware to device (requires PORT variable)"
	@echo "  install-deps  - Install build dependencies"
	@echo "  test          - Run basic syntax check"
	@echo ""
	@echo "Usage examples:"
	@echo "  make build"
	@echo "  make build-esp8266"
	@echo "  make PORT=/dev/ttyUSB0 flash"
	@echo "  make install-deps"

# Install dependencies
install-deps:
	pip install mpy-cross esptool

# Build targets
build: build-esp8266 build-esp32

build-esp8266:
	./build.sh esp8266

build-esp32:
	./build.sh esp32

# Clean build artifacts
clean:
	rm -rf build/
	rm -f code/main.mpy

# Flash firmware (requires PORT variable)
flash:
	@if [ -z "$(PORT)" ]; then \
		echo "Error: PORT variable not set. Use: make PORT=/dev/ttyUSB0 flash"; \
		exit 1; \
	fi
	@echo "Flashing to $(PORT)..."
	@if [ -f "build/main.mpy" ]; then \
		esptool.py --port $(PORT) --baud 115200 write_flash 0x100000 build/main.mpy; \
	else \
		echo "Error: Build firmware first with 'make build'"; \
		exit 1; \
	fi

# Basic syntax check
test:
	python -m py_compile code/main.py
	@echo "Syntax check passed"
