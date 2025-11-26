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
DNS_PROVIDERS_IPV4 = ["9.9.9.9", "1.1.1.1", "8.8.8.8", "94.140.14.14", "76.76.19.19", "76.76.2.0", "185.228.168.9",
                     "208.67.222.222", "80.80.80.80"]

# Unique device identifier
DEVICE_IDENTIFIER = "DNS-mixer"

# Pin configuration
LED = machine.Pin(2, machine.Pin.OUT)

# Function to connect to WiFi
def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    # Set static IP but don't configure DNS (let it use default or none)
    # This prevents conflicts since this device IS the DNS server
    sta_if.ifconfig((STATIC_IP, "255.255.255.0", "192.168.8.1", None))
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

    while not sta_if.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)

    print("Connected to WiFi")

    blink(5, 0.2, 0.3)  # Blink 5 times with 0.2s on and 0.3s off

# Function to handle LED blinking
def blink(num_blinks, on_duration, off_duration):
    for _ in range(num_blinks):
        LED.value(1)
        time.sleep(on_duration)
        LED.value(0)
        time.sleep(off_duration)

# Function to handle DNS requests with load balancing
def handle_dns_request(data, addr):
    import urandom

    print("Received DNS request from:", addr)

    blink(1, 0.05, 0)  # Blink for 0.05s on new request

    success = False

    # Shuffle DNS providers for load balancing and redundancy
    shuffled_providers = DNS_PROVIDERS_IPV4.copy()
    for i in range(len(shuffled_providers) - 1, 0, -1):
        j = int(urandom.getrandbits(8) % (i + 1))
        shuffled_providers[i], shuffled_providers[j] = shuffled_providers[j], shuffled_providers[i]

    # Try each DNS provider in randomized order
    for dns_provider in shuffled_providers:
        print("Trying DNS provider:", dns_provider)

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
            break
        except Exception as e:
            print("Failed to resolve using DNS provider:", dns_provider, "Error:", str(e))
        finally:
            dns_socket.close()

    if not success:
        blink(1, 0.5, 0)  # Blink for 0.5s on failure
        print("Failed to forward DNS request - all providers unreachable")

    return success

# Connect to WiFi
connect_to_wifi()

# Create a UDP socket for DNS
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 53))

# Initialize the OLED display
i2c = I2C(sda=Pin(4), scl=Pin(5))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize counters
total_requests = 0
total_success = 0
total_reject = 0

# Main loop to handle DNS requests
while True:
    data, addr = server_socket.recvfrom(1024)
    success = handle_dns_request(data, addr)

    # Update counters
    total_requests += 1
    if success:
        total_success += 1
    else:
        total_reject += 1

    # Update OLED display with counters and device identifier
    oled.fill(0)
    oled.text(DEVICE_IDENTIFIER, 30, 0, 1)
    oled.text("IP:" + STATIC_IP, 0, 12, 1)
    oled.text("Total: " + str(total_requests), 0, 24, 1)
    oled.text("Success: " + str(total_success), 0, 36, 1)
    oled.text("Reject: " + str(total_reject), 0, 48, 1)
    oled.show()

    # Sleep for a short duration to handle requests
    time.sleep(0.03)
