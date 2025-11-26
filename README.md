# DNS Mixer

Welcome to DNS-mixer! This is a MicroPython-based DNS forwarding service for ESP8266/ESP32 devices with OLED display support. The service handles DNS requests and forwards them to multiple DNS providers, ensuring reliability and redundancy in DNS resolution.

> **Quick Start**: New users should start with the [setup guides](setup/README.md) for comprehensive installation and configuration instructions.

## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Hardware Setup](#hardware-setup)
4. [Configuration](#configuration)
    - [WiFi Configuration](#wifi-configuration)
    - [DNS Providers](#dns-providers)
5. [Building and Flashing](#building-and-flashing)
6. [Usage](#usage)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

DNS-mixer is a MicroPython-based DNS resolver for ESP8266/ESP32 devices that intelligently routes DNS queries through multiple DNS providers to bypass restrictions and ensure reliable name resolution. The device acts as a DNS server on your network, providing redundancy and failover capabilities.

### Key Features

- **Multi-Provider Failover**: Cycles through 9+ DNS providers (Quad9, Cloudflare, Google DNS, etc.) for maximum reliability
- **Load Balancing**: Randomizes provider order to distribute load and avoid single points of failure
- **Restriction Bypass**: Works around DNS blocking by trying multiple providers until one succeeds
- **Router Integration**: Configure as DNS server in router settings for network-wide protection
- **Real-time Monitoring**: OLED display shows live statistics and connection status
- **Low Resource Usage**: Optimized for ESP8266/ESP32 with minimal memory footprint

## Requirements

- ESP8266 or ESP32 development board
- SSD1306 OLED display (128x64, I2C)
- MicroPython firmware installed on the device
- Network connectivity between the ESP device and client devices

## Hardware Setup

### OLED Display Connection
- SDA: GPIO 4 (D2 on ESP8266)
- SCL: GPIO 5 (D1 on ESP8266)
- VCC: 3.3V
- GND: GND

> **Detailed Setup Guide**: See [setup/server.md](setup/server.md) for comprehensive hardware setup instructions, wiring diagrams, and both automated and manual installation methods.

### ESP32 vs ESP8266 Comparison

| Feature | ESP8266 | ESP32 |
|---------|---------|--------|
| **Processor** | 32-bit RISC (80 MHz) | Dual-core 32-bit (160-240 MHz) |
| **RAM** | 80 KB | 520 KB |
| **Flash** | External (up to 16 MB) | External (up to 16 MB) |
| **WiFi** | 802.11 b/g/n (2.4 GHz only) | 802.11 b/g/n (2.4 GHz) + Bluetooth 4.2 |
| **GPIO Pins** | 17 | 34 |
| **ADC Channels** | 1 (10-bit) | 18 (12-bit) |
| **PWM Channels** | 4 | 16 |
| **I2C** | 1 | 2 |
| **SPI** | 1 | 4 |
| **UART** | 1 | 3 |
| **Power Consumption** | Lower | Higher |
| **Cost** | Lower (~$2-3) | Higher (~$4-6) |
| **MicroPython Performance** | Good for simple tasks | Better for complex applications |
| **DNS-mixer Suitability** | Excellent (simpler, cheaper) | Excellent (more powerful, faster) |

**Recommendation**: Use ESP8266 for cost-effective deployments. Use ESP32 for more demanding applications or when you need Bluetooth connectivity.

## Configuration

### WiFi Configuration

Edit the WiFi settings in `code/main.py` to match your network credentials:

```python
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"
STATIC_IP = "192.168.1.100"  # Choose an available IP in your network
```

### DNS Providers

The device includes 9 pre-configured DNS providers optimized for reliability and restriction bypass:

```python
DNS_PROVIDERS_IPV4 = [
    "9.9.9.9",        # Quad9 (Malware blocking)
    "1.1.1.1",        # Cloudflare (Fast, privacy-focused)
    "8.8.8.8",        # Google DNS (Widely accessible)
    "94.140.14.14",   # AdGuard DNS (Ad blocking)
    "76.76.19.19",    # Alternate DNS (Uncensored)
    "76.76.2.0",      # Control D (Uncensored)
    "185.228.168.9",  # CleanBrowsing (Security)
    "208.67.222.222", # OpenDNS (Reliable)
    "80.80.80.80"     # Freenom (Alternative)
]
```

**Provider Benefits for Bypass:**
- **Multiple Countries**: Providers from different jurisdictions reduce blocking likelihood
- **Privacy-Focused**: Quad9, Cloudflare offer enhanced privacy
- **Uncensored Options**: Alternate DNS, Control D provide unrestricted access
- **Failover Speed**: 50ms timeout ensures quick switching between providers

> **Advanced Configuration**: For detailed configuration options, custom DNS providers, and advanced settings, see [setup/server.md](setup/server.md#configuration).

## Building and Flashing

### Quick Start (Recommended)

Use the provided Makefile for easy building:

```bash
# Install build dependencies
make install-deps

# Build for both ESP8266 and ESP32 (default)
make build

# Or build for specific target
make build-esp8266
make build-esp32
```

### Using Build Script

The project includes automated build scripts for both boards:

```bash
# Build for ESP8266
./build.sh esp8266

# Build for ESP32
./build.sh esp32
```

### Manual Build

1. Install dependencies:
```bash
pip install mpy-cross esptool
```

2. Compile the main script:
```bash
mpy-cross code/main.py
```

### Flashing to Device

After building, use the deployment script or flash manually:

```bash
# Using the deployment script (recommended)
cd build && ./deploy.sh /dev/ttyUSB0 esp8266

# Or using make (after building)
make PORT=/dev/ttyUSB0 flash

# Manual flashing with esptool
esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect 0 esp8266-firmware.bin
esptool.py --port /dev/ttyUSB0 --baud 115200 --after no_reset write_flash --flash_size=detect 0x100000 build/main.mpy
```

### Automated Builds

The project includes GitHub Actions workflows for automated building:

- **Development builds**: Trigger on every push to main/master branch
- **Release builds**: Trigger on version tags (v*) and create GitHub releases with firmware archives

> **Complete Flashing Guide**: For detailed flashing instructions, troubleshooting, and alternative methods (including Thonny IDE), see [setup/server.md](setup/server.md#flashing-and-testing).

## Usage

### Basic Operation

The device will automatically:
1. Connect to the configured WiFi network
2. Start the DNS server on port 53
3. Display connection status and statistics on the OLED screen
4. Forward DNS requests to configured providers with failover

### Router Configuration for Network-Wide DNS

To use DNS-mixer network-wide, configure your router to use it as the DNS server:

#### 1. Access Router Admin Panel
- Open browser and go to your router's IP (usually 192.168.1.1 or 192.168.0.1)
- Login with admin credentials

#### 2. Configure DNS Settings
Look for DNS settings in:
- **Network Settings > DHCP Settings**
- **Advanced > Network > DNS**
- **WAN Settings > DNS Configuration**

Set the **Primary DNS** to your DNS-mixer's IP address (default: `192.168.8.180`)

> **Router Setup Guide**: For detailed router configuration instructions for ASUS, TP-Link, Netgear, and other brands, see [setup/otherdevices.md](setup/otherdevices.md#router-configuration-network-wide).

#### 3. Alternative: Device-Level Configuration
Configure individual devices to use DNS-mixer:
- **Windows**: Network Settings > Change adapter options > Properties > IPv4 > DNS server
- **macOS**: System Preferences > Network > Advanced > DNS
- **Linux**: Edit `/etc/resolv.conf` or network manager
- **Mobile**: WiFi settings > Modify network > Advanced > DNS

> **Device Configuration Guide**: For step-by-step instructions for Windows, macOS, Linux, mobile devices, gaming consoles, and smart TVs, see [setup/otherdevices.md](setup/otherdevices.md).

### Bypassing Restrictions

DNS-mixer helps bypass DNS-based restrictions by:

1. **Provider Failover**: If one DNS provider is blocked, it automatically tries others
2. **Load Balancing**: Distributes requests across providers to avoid detection
3. **Fast Switching**: 50ms timeout ensures quick fallback to working providers
4. **Multiple Providers**: 9+ providers including international ones (Quad9, Cloudflare, Google, AdGuard, etc.)

### LED Indicators
- **5 blinks**: Device connected to WiFi
- **1 short blink**: DNS request received
- **1 very short blink**: DNS resolution successful
- **1 long blink**: DNS resolution failed (all providers unreachable)

## Troubleshooting

> **Detailed Troubleshooting**: For comprehensive troubleshooting guides including hardware issues, WiFi problems, DNS resolution failures, and device-specific problems, see:
> - [setup/server.md](setup/server.md#troubleshooting) - ESP device setup issues
> - [setup/otherdevices.md](setup/otherdevices.md#troubleshooting) - Client device configuration problems

### Quick Troubleshooting Tips

If you encounter issues:
- Verify OLED display shows connection status and IP address
- Check LED indicators for error patterns
- Test DNS resolution with `nslookup google.com [DNS_MIXER_IP]`
- Ensure DNS-mixer IP is in your router's subnet
- Monitor serial output for error messages

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Your feedback and improvements are highly appreciated.

## License

This project is licensed under the [MIT License](LICENSE).
