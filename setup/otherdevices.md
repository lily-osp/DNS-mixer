# Setting Up DNS on Other Devices

This guide explains how to configure various devices and systems to use your DNS-mixer as their DNS server, enabling network-wide DNS resolution with bypass capabilities.

## Table of Contents

1. [Router Configuration (Network-Wide)](#router-configuration-network-wide)
2. [Windows Configuration](#windows-configuration)
3. [macOS Configuration](#macos-configuration)
4. [Linux Configuration](#linux-configuration)
5. [Mobile Devices](#mobile-devices)
6. [Smart TVs and Gaming Consoles](#smart-tvs-and-gaming-consoles)
7. [Verification and Testing](#verification-and-testing)
8. [Troubleshooting](#troubleshooting)

## Router Configuration (Network-Wide)

**Recommended Method** - Configure your router to use DNS-mixer for all devices on your network automatically.

### Find Your Router's IP Address

- **Windows**: Open Command Prompt -> `ipconfig` -> Look for "Default Gateway"
- **macOS**: System Preferences -> Network -> Advanced -> TCP/IP -> Router
- **Linux**: `ip route show` or check `/etc/resolv.conf`

Common router IPs: `192.168.1.1`, `192.168.0.1`, `10.0.0.1`

### Access Router Admin Panel

1. Open web browser
2. Enter router IP address
3. Login with admin credentials (default: admin/admin or admin/password)

### Configure DNS Settings

**Location varies by router brand:**

#### ASUS Routers
1. `Advanced Settings` -> `WAN` -> `Internet Connection`
2. Set `DNS Server` to your DNS-mixer's IP (e.g., `192.168.1.100`)

#### TP-Link Routers
1. `Network` -> `WAN` -> `Dynamic IP`
2. Set `Primary DNS` to your DNS-mixer's IP

#### Netgear Routers
1. `Advanced` -> `Setup` -> `Internet Setup`
2. Set `DNS Address` to your DNS-mixer's IP

#### Generic Router Steps
1. Look for `DNS`, `DHCP`, or `Network Settings`
2. Find `DNS Server` or `Name Server` configuration
3. Set **Primary DNS** to your DNS-mixer's static IP
4. Leave **Secondary DNS** blank or set to another reliable DNS

### Save and Reboot
1. Save changes
2. Reboot router if required
3. All devices on network will now use DNS-mixer automatically

## Windows Configuration

### Windows 10/11

1. **Right-click Start button** -> **Settings**
2. **Network & Internet** -> **Status**
3. **Change adapter options** (bottom right)
4. **Right-click your network connection** -> **Properties**
5. **Internet Protocol Version 4 (TCP/IPv4)** -> **Properties**
6. Select **"Use the following DNS server addresses"**
7. **Preferred DNS server**: Enter your DNS-mixer's IP (e.g., `192.168.1.100`)
8. **Alternate DNS server**: Leave blank or use `1.1.1.1`
9. Click **OK** -> **Close**

### Windows 7/8

1. **Control Panel** -> **Network and Sharing Center**
2. **Change adapter settings** (left side)
3. **Right-click your connection** -> **Properties**
4. **Internet Protocol Version 4 (TCP/IPv4)** -> **Properties**
5. Select **"Use the following DNS server addresses"**
6. **Preferred DNS server**: DNS-mixer IP
7. Click **OK** -> **Close**

### Command Line Method (All Windows)

```cmd
# Set DNS for Ethernet
netsh interface ipv4 set dns "Ethernet" static 192.168.1.100

# Set DNS for WiFi
netsh interface ipv4 set dns "Wi-Fi" static 192.168.1.100
```

## macOS Configuration

### macOS Monterey (12.0+) / Ventura (13.0+) / Sonoma (14.0+)

1. **System Settings** -> **Network**
2. Select your network connection (Wi-Fi or Ethernet)
3. Click **Details...** button
4. Select **DNS** tab
5. Click **+** button to add DNS server
6. Enter your DNS-mixer's IP address
7. Click **OK** -> **Apply**

### Older macOS Versions

1. **System Preferences** -> **Network**
2. Select your connection -> **Advanced...**
3. **DNS** tab -> **+** button
4. Enter DNS-mixer IP address
5. **OK** -> **Apply**

### Terminal Method

```bash
# Edit resolv.conf (temporary, resets on reboot)
sudo bash -c 'echo "nameserver 192.168.1.100" > /etc/resolv.conf'

# Or use networksetup
networksetup -setdnsservers Wi-Fi 192.168.1.100
networksetup -setdnsservers Ethernet 192.168.1.100
```

## Linux Configuration

### Ubuntu/Debian (Network Manager)

1. **Settings** -> **Network** (or `nm-connection-editor`)
2. Select your connection -> **Settings** (gear icon)
3. **IPv4** tab → **DNS** section
4. Set to **Manual**
5. Enter DNS-mixer IP in DNS servers field
6. **Save** -> **Turn off/on** the connection

### Ubuntu/Debian (Netplan - Server Edition)

Edit `/etc/netplan/01-netcfg.yaml`:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
      nameservers:
        addresses: [192.168.1.100]
```

```bash
sudo netplan apply
```

### Red Hat/CentOS/Fedora

Edit `/etc/resolv.conf`:

```bash
sudo bash -c 'echo "nameserver 192.168.1.100" >> /etc/resolv.conf'
```

Or for permanent change, edit `/etc/sysconfig/network-scripts/ifcfg-eth0`:

```
DNS1=192.168.1.100
```

### Arch Linux

Edit `/etc/resolv.conf`:

```bash
sudo bash -c 'echo "nameserver 192.168.1.100" >> /etc/resolv.conf'
```

Make it persistent by disabling systemd-resolved and using dhcpcd or NetworkManager.

## Mobile Devices

### Android

1. **Settings** -> **Network & internet** -> **Wi-Fi**
2. Long-press your Wi-Fi network -> **Modify network**
3. **Advanced options** → **IP settings** → **Static**
4. Scroll down to **DNS 1**
5. Enter DNS-mixer IP address
6. **Save**

### iOS/iPadOS

1. **Settings** -> **Wi-Fi**
2. Tap **Info (i)** next to your network name
3. Scroll down to **Configure DNS**
4. Select **Manual**
5. Delete existing DNS servers
6. Tap **Add Server**
7. Enter DNS-mixer IP address
8. **Save**

## Smart TVs and Gaming Consoles

### Smart TVs (Samsung, LG, etc.)

1. **Settings** -> **Network** -> **Network Status**
2. Select your network -> **IP Settings**
3. Set DNS to **Manual**
4. Enter DNS-mixer IP as DNS server

### PlayStation 4/5

1. **Settings** -> **Network** -> **Settings**
2. Select your connection -> **Advanced Settings**
3. **IP Address Settings** -> **Manual**
4. Set **DNS** to **Manual**
5. **Primary DNS**: DNS-mixer IP
6. **Secondary DNS**: Leave blank

### Xbox One/Series X|S

1. **Settings** -> **Network** -> **Network settings**
2. Select your network -> **Advanced settings**
3. **DNS settings** -> **Manual**
4. **Primary DNS**: DNS-mixer IP
5. **Secondary DNS**: Optional

## Verification and Testing

### Test DNS Resolution

**Windows:**
```cmd
nslookup google.com
```

**macOS/Linux:**
```bash
dig google.com
# or
nslookup google.com
```

**Expected output should show:**
- DNS server responding from your DNS-mixer's IP
- Successful resolution of domains

### Test Bypass Functionality

Try accessing domains that might be restricted:

```bash
nslookup twitter.com
nslookup youtube.com
nslookup github.com
```

If one provider is blocked, DNS-mixer should automatically try others.

### Monitor DNS-Mixer

Check the OLED display on your ESP device for:
- Connection status
- Request counters
- Success/failure statistics

## Troubleshooting

### DNS Not Working

1. **Verify DNS-mixer is running**:
   - Check OLED display shows IP and statistics
   - LED should blink with DNS requests

2. **Check connectivity**:
   ```bash
   ping [DNS_MIXER_IP]
   ```

3. **Verify configuration**:
   - Ensure DNS-mixer IP is correct
   - Check network subnet matches

4. **Clear DNS cache**:
   - **Windows**: `ipconfig /flushdns`
   - **macOS**: `sudo killall -HUP mDNSResponder`
   - **Linux**: `sudo systemd-resolve --flush-caches`

### Slow Resolution

- DNS-mixer uses 50ms timeout per provider
- With 9 providers, maximum delay is ~450ms
- This is normal for maximum reliability

### Intermittent Issues

- Check WiFi signal strength
- Verify DNS-mixer has stable power
- Monitor OLED for error statistics

### Router Not Accepting Changes

- Some routers require reboot after DNS changes
- Try factory reset if configuration won't save
- Check for firmware updates

If issues persist, refer to the main README.md troubleshooting section or check the serial output of your DNS-mixer device.
