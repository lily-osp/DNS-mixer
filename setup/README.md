# DNS-Mixer Setup Guides

This directory contains comprehensive setup guides for configuring your DNS-mixer ESP8266/ESP32 device and connecting other devices to use it.

## Available Guides

### [Server Setup (`server.md`)](server.md)
Complete guide for setting up your ESP8266/ESP32 as a DNS-mixer resolver:
- Hardware requirements and wiring
- MicroPython firmware installation
- Automated and manual build processes
- Configuration and flashing
- Testing and troubleshooting

### [Device Configuration (`otherdevices.md`)](otherdevices.md)
Instructions for configuring various devices to use your DNS-mixer:
- Router configuration (network-wide setup)
- Windows, macOS, and Linux configuration
- Mobile devices (Android/iOS)
- Smart TVs and gaming consoles
- Verification and testing procedures

## Quick Start

1. **Set up your DNS-mixer**: Follow [`server.md`](server.md) to configure your ESP device
2. **Configure your router**: Use [`otherdevices.md`](otherdevices.md) for network-wide DNS
3. **Test the setup**: Verify DNS resolution is working correctly
4. **Monitor performance**: Check the OLED display for statistics

## Support

If you encounter issues:
- Check the troubleshooting sections in each guide
- Verify your hardware connections
- Ensure your DNS-mixer IP is accessible on the network
- Monitor the device serial output for error messages

For additional help, refer to the main project [README.md](../README.md).
