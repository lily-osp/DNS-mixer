import network
import socket
import machine
import time
from machine import I2C, Pin
import ssd1306

# Constants
WIFI_SSID = "bayar"
WIFI_PASSWORD = "drowssap"
STATIC_IP = "192.168.8.180"
DNS_PROVIDERS_IPV4 = [
    "9.9.9.9", 
    "1.1.1.1", 
    "8.8.8.8", 
    "94.140.14.14", 
    "76.76.19.19", 
    "76.76.2.0", 
    "185.228.168.9",
    "208.67.222.222", 
    "80.80.80.80"
]

# Unique device identifier
DEVICE_IDENTIFIER = "DNS-mixer"

# Pin configuration
LED = machine.Pin(2, machine.Pin.OUT)

# Function to connect to WiFi
def connect_to_wifi():
    global oled
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    # Set static IP but don't configure DNS (let it use default or none)
    # This prevents conflicts since this device IS the DNS server
    sta_if.ifconfig((STATIC_IP, "255.255.255.0", "192.168.8.1", None))
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

    print("Connecting to WiFi...")
    update_oled_status("connecting")

    while not sta_if.isconnected():
        print("Still connecting...")
        time.sleep(1)

    print("Connected to WiFi")

    # Show connection animation
    animate_connection()

    blink(5, 0.2, 0.3)  # Blink 5 times with 0.2s on and 0.3s off

# Function to handle LED blinking
def blink(num_blinks, on_duration, off_duration):
    for _ in range(num_blinks):
        LED.value(1)
        time.sleep(on_duration)
        LED.value(0)
        time.sleep(off_duration)

# OLED Animation and Status Functions
def update_oled_status(status, progress=None, provider=None, request_count=None):
    """Update OLED with detailed status information and animations"""
    oled.fill(0)

    # Header with device identifier
    oled.text(DEVICE_IDENTIFIER, 25, 0, 1)

    # IP Address
    oled.text("IP:" + STATIC_IP, 0, 12, 1)

    # Status line with animation
    if status == "connecting":
        # Animated connecting dots
        dots = "." * ((int(time.time() * 2) % 4))
        oled.text("Connecting" + dots, 0, 24, 1)
        oled.text("to WiFi...", 0, 36, 1)
    elif status == "connected":
        oled.text("WiFi Connected!", 0, 24, 1)
        oled.text("Starting DNS...", 0, 36, 1)
    elif status == "ready":
        oled.text("DNS Server Ready", 0, 24, 1)
        oled.text("Waiting requests", 0, 36, 1)
    elif status == "processing":
        # Animated processing indicator
        spinner = "|/-\\"[(int(time.time() * 4) % 4)]
        oled.text("Processing" + spinner, 0, 24, 1)
        if provider:
            # Truncate long provider names
            short_provider = provider.replace("208.67.222.222", "OpenDNS").replace("185.228.168.9", "CleanBrws")
            if len(short_provider) > 12:
                short_provider = short_provider[:9] + "..."
            oled.text(short_provider, 0, 36, 1)
        else:
            oled.text("DNS Request", 0, 36, 1)
    elif status == "success":
        oled.text("Resolution OK", 0, 24, 1)
        if provider:
            short_provider = provider.replace("208.67.222.222", "OpenDNS").replace("185.228.168.9", "CleanBrws")
            if len(short_provider) > 12:
                short_provider = short_provider[:9] + "..."
            oled.text("Via: " + short_provider, 0, 36, 1)
    elif status == "failed":
        oled.text("Resolution Failed", 0, 24, 1)
        oled.text("All providers down", 0, 36, 1)
    elif status == "stats":
        # Statistics view
        oled.text("Total: " + str(total_requests), 0, 24, 1)
        oled.text("Success: " + str(total_success), 0, 36, 1)
        oled.text("Failed: " + str(total_reject), 0, 48, 1)

    # Progress bar for operations (if provided)
    if progress is not None and 0 <= progress <= 100:
        bar_width = int((progress / 100) * 128)
        oled.rect(0, 56, 128, 8, 1)  # Border
        oled.fill_rect(2, 58, bar_width - 4 if bar_width > 4 else 0, 4, 1)  # Fill

    oled.show()

def animate_connection():
    """Animated connection sequence"""
    for i in range(10):
        progress = (i + 1) * 10
        update_oled_status("connecting", progress)
        time.sleep(0.5)
    update_oled_status("connected")
    time.sleep(1)
    update_oled_status("ready")

# Function to handle DNS requests with load balancing
def handle_dns_request(data, addr):
    import urandom

    print("Received DNS request from:", addr)

    # Show processing status on OLED
    update_oled_status("processing")

    blink(1, 0.05, 0)  # Blink for 0.05s on new request

    success = False
    last_provider = None

    # Shuffle DNS providers for load balancing and redundancy
    shuffled_providers = DNS_PROVIDERS_IPV4.copy()
    for i in range(len(shuffled_providers) - 1, 0, -1):
        j = int(urandom.getrandbits(8) % (i + 1))
        shuffled_providers[i], shuffled_providers[j] = shuffled_providers[j], shuffled_providers[i]

    # Try each DNS provider in randomized order
    for dns_provider in shuffled_providers:
        print("Trying DNS provider:", dns_provider)

        # Update OLED with current provider
        update_oled_status("processing", provider=dns_provider)
        last_provider = dns_provider

        # Create a UDP socket to forward the DNS request
        dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dns_socket.settimeout(0.05)  # Slightly longer timeout for better reliability

        try:
            dns_socket.sendto(data, (dns_provider, 53))
            response, _ = dns_socket.recvfrom(1024)
            # Forward the DNS response to the original requester
            server_socket.sendto(response, addr)
            blink(1, 0.02, 0)  # Blink for 0.02s on success
            success = True
            print("Success using DNS provider:", dns_provider)

            # Show success status briefly
            update_oled_status("success", provider=dns_provider)
            time.sleep(0.5)  # Show success message for half second
            break
        except Exception as e:
            print("Failed to resolve using DNS provider:", dns_provider, "Error:", str(e))
        finally:
            dns_socket.close()

    if not success:
        blink(1, 0.5, 0)  # Blink for 0.5s on failure
        print("Failed to forward DNS request - all providers unreachable")

        # Show failure status briefly
        update_oled_status("failed")
        time.sleep(1)  # Show failure message for 1 second

    return success

# Initialize counters
total_requests = 0
total_success = 0
total_reject = 0

# Initialize the OLED display
i2c = I2C(sda=Pin(4), scl=Pin(5))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Connect to WiFi
connect_to_wifi()

# Create a UDP socket for DNS
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 53))

print("DNS server started on port 53")

# Show ready status
update_oled_status("ready")

# Main loop to handle DNS requests
last_stats_update = time.time()
stats_display_duration = 5  # Show stats for 5 seconds
showing_stats = False

while True:
    try:
        # Non-blocking socket check with timeout
        server_socket.settimeout(0.1)  # Check for requests every 100ms
        data, addr = server_socket.recvfrom(1024)
        success = handle_dns_request(data, addr)

        # Update counters
        total_requests += 1
        if success:
            total_success += 1
        else:
            total_reject += 1

        # Reset stats display timer
        last_stats_update = time.time()
        showing_stats = False

    except:
        # No request received, continue to stats display logic
        pass

    # Update OLED display
    current_time = time.time()

    # Show stats periodically or after a period of inactivity
    if not showing_stats and (current_time - last_stats_update) > 3:
        update_oled_status("stats")
        showing_stats = True
    elif showing_stats and (current_time - last_stats_update) > stats_display_duration:
        update_oled_status("ready")
        showing_stats = False

    # Sleep for a short duration
    time.sleep(0.03)
