# Setting Up ESP8266/ESP32 as DNS Provider

This comprehensive guide provides step-by-step instructions for setting up your ESP8266 or ESP32 as a DNS-mixer resolver using MicroPython. The DNS-mixer acts as a smart DNS server that intelligently routes queries through multiple providers for redundancy and restriction bypass.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Method 1: Automated Setup (Recommended)](#method-1-automated-setup-recommended)
3. [Method 2: Manual Setup](#method-2-manual-setup)
4. [Hardware Wiring](#hardware-wiring)
5. [Configuration](#configuration)
6. [Flashing and Testing](#flashing-and-testing)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting, ensure you have:

- **ESP8266 or ESP32 development board**
- **SSD1306 OLED display** (128x64, I2C interface)
- **Computer with USB port** for flashing
- **Micro-USB cable** compatible with your ESP board
- **WiFi network** with internet access
- **Python 3.x** installed on your computer

### Required Software
- **esptool** for flashing firmware
- **mpy-cross** for compiling MicroPython code
- **Terminal/Shell** access

## Method 1: Automated Setup (Recommended)

The easiest way to set up your DNS-mixer:

### 1. Clone and Build

```bash
git clone https://github.com/your-repo/dns-mixer.git
cd dns-mixer
make install-deps
make build-esp8266  # or make build-esp32
```

### 2. Configure WiFi

Edit `code/main.py` and update these variables:

```python
WIFI_SSID = "Your_WiFi_Name"
WIFI_PASSWORD = "Your_WiFi_Password"
STATIC_IP = "192.168.1.100"  # Choose unused IP in your network range
```

### 3. Flash to Device

```bash
# Connect your ESP device
ls /dev/ttyUSB*  # Find your device port

# Flash the firmware
make PORT=/dev/ttyUSB0 flash
```

## Method 2: Manual Setup

For manual setup without the build system:

### 1. Install MicroPython Firmware

#### Download Firmware
Visit [MicroPython Downloads](https://micropython.org/download/) and download:
- **ESP8266**: `esp8266-20220618-v1.19.1.bin` or latest
- **ESP32**: `esp32-20220618-v1.19.1.bin` or latest

#### Flash Firmware
```bash
# Install esptool if not already installed
pip install esptool

# Flash ESP8266
esptool.py --chip esp8266 --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect 0x0 esp8266-20220618-v1.19.1.bin

# Flash ESP32
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect 0x1000 esp32-20220618-v1.19.1.bin
```

### 2. Alternative: Using Thonny IDE

1. Download and install [Thonny IDE](https://thonny.org/)
2. Connect your ESP board
3. In Thonny: `Tools -> Options -> Interpreter`
4. Select `MicroPython (ESP8266/ESP32)` and your port
5. Thonny will automatically install the firmware

## Hardware Wiring

### OLED Display Connection

| OLED Pin | ESP8266 Pin | ESP32 Pin | Description |
|----------|-------------|-----------|-------------|
| VCC      | 3.3V       | 3.3V     | Power supply |
| GND      | GND        | GND      | Ground      |
| SCL      | GPIO 5 (D1)| GPIO 22  | I2C Clock   |
| SDA      | GPIO 4 (D2)| GPIO 21  | I2C Data    |

### LED Connection (Optional)
- Connect LED to **GPIO 2** (built-in LED on most boards)
- Or connect external LED to any available GPIO pin

## Configuration

### Basic Configuration

Edit the following variables in `code/main.py`:

```python
# WiFi Settings
WIFI_SSID = "Your_WiFi_Name"
WIFI_PASSWORD = "Your_WiFi_Password"
STATIC_IP = "192.168.1.100"  # Must be in your router's subnet

# Device Identity
DEVICE_IDENTIFIER = "DNS-mixer"

# DNS Providers (9 providers for maximum redundancy)
DNS_PROVIDERS_IPV4 = [
    "9.9.9.9",        # Quad9
    "1.1.1.1",        # Cloudflare
    "8.8.8.8",        # Google
    "94.140.14.14",   # AdGuard
    "76.76.19.19",    # Alternate DNS
    "76.76.2.0",      # Control D
    "185.228.168.9",  # CleanBrowsing
    "208.67.222.222", # OpenDNS
    "80.80.80.80"     # Freenom
]
```

### Advanced Configuration

```python
# DNS timeout per provider (milliseconds)
DNS_TIMEOUT = 0.05

# LED pin (use 2 for built-in LED, or your external LED pin)
LED_PIN = 2
```

## Flashing and Testing

### Upload Code to ESP

#### Using ampy (Command Line)
```bash
pip install adafruit-ampy

# Compile to .mpy for better performance
mpy-cross code/main.py

# Upload to ESP
ampy -p /dev/ttyUSB0 put code/main.mpy
```

#### Using Thonny IDE
1. Open `code/main.py` in Thonny
2. Connect to your ESP board
3. Click `Run` or save directly to device

### Verify Operation

1. **Check Serial Output**:
   ```
   Connecting to WiFi...
   Connected to WiFi
   ```

2. **Monitor OLED Display**:
   - Shows device IP and real-time statistics
   - Updates with each DNS request

3. **LED Indicators**:
   - **5 blinks**: Connected to WiFi
   - **1 short blink**: DNS request received
   - **1 very short blink**: DNS resolution successful
   - **1 long blink**: All providers failed

### Test DNS Resolution

```bash
# On another device in the same network
nslookup google.com 192.168.1.100  # Use your DNS-mixer's IP
```

## Troubleshooting

### Common Issues

#### 1. WiFi Connection Failed
- Check SSID and password in `code/main.py`
- Verify WiFi signal strength
- Try different WiFi channel

#### 2. No DNS Responses
- Verify static IP is in router's subnet
- Check if port 53 is available (no other DNS server running)
- Test with `ping [DNS_MIXER_IP]` from another device

#### 3. OLED Display Not Working
- Verify I2C connections (SDA, SCL, VCC, GND)
- Check OLED address (usually 0x3C)
- Try different I2C pins if using ESP32

#### 4. Import Errors
- Ensure `ssd1306.py` is available on the device
- Upload required libraries: `ssd1306.mpy`

#### 5. Device Not Accessible
- Check USB port permissions (`ls -la /dev/ttyUSB*`)
- Try different USB cable
- Verify board is not in bootloader mode

### Debug Mode

Enable debug output by modifying the code:

```python
# Add debug prints
print("DNS Request:", data[:20])  # First 20 bytes
print("Response from:", dns_provider)
```

### Recovery

If device becomes unresponsive:
1. Hold BOOT/FLASH button while plugging in
2. Re-flash MicroPython firmware
3. Re-upload DNS-mixer code

## Next Steps

Once your DNS-mixer is running:
1. Configure your router to use it as DNS server
2. Set up other devices to use the DNS-mixer IP
3. Monitor the OLED display for statistics
4. Enjoy unrestricted, reliable DNS resolution!

For advanced configuration and customization, refer to the main README.md file.
