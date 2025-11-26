#!/bin/bash

# DNS-mixer Build Script
# Compiles MicroPython code and creates firmware images for ESP8266/ESP32

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
SOURCE_FILE="$SCRIPT_DIR/code/main.py"
MICROPYTHON_VERSION="1.19.1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if target is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <esp8266|esp32>"
    exit 1
fi

TARGET=$1

# Validate target
if [[ "$TARGET" != "esp8266" && "$TARGET" != "esp32" ]]; then
    log_error "Invalid target. Use 'esp8266' or 'esp32'"
    exit 1
fi

log_info "Building DNS-mixer for $TARGET"

# Create build directory
mkdir -p "$BUILD_DIR"

# Check if mpy-cross is installed
if ! command -v mpy-cross &> /dev/null; then
    log_error "mpy-cross not found. Install with: pip install mpy-cross"
    exit 1
fi

# Check if source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    log_error "Source file not found: $SOURCE_FILE"
    exit 1
fi

# Compile to .mpy
log_info "Compiling main.py to bytecode..."
mpy-cross "$SOURCE_FILE"

if [ ! -f "${SOURCE_FILE%.py}.mpy" ]; then
    log_error "Failed to compile main.py"
    exit 1
fi

# Move compiled file to build directory
mv "${SOURCE_FILE%.py}.mpy" "$BUILD_DIR/main.mpy"

# Create firmware image name
FIRMWARE_NAME="dns-mixer-${TARGET}-$(date +%Y%m%d-%H%M%S).bin"
FIRMWARE_PATH="$BUILD_DIR/$FIRMWARE_NAME"

# Download base MicroPython firmware if it doesn't exist
BASE_FIRMWARE_DIR="$SCRIPT_DIR/firmware"
mkdir -p "$BASE_FIRMWARE_DIR"

if [ "$TARGET" = "esp8266" ]; then
    BASE_FIRMWARE_URL="https://micropython.org/resources/firmware/esp8266-20220618-v1.19.1.bin"
    BASE_FIRMWARE_FILE="$BASE_FIRMWARE_DIR/esp8266-v$MICROPYTHON_VERSION.bin"
else
    BASE_FIRMWARE_URL="https://micropython.org/resources/firmware/esp32-20220618-v1.19.1.bin"
    BASE_FIRMWARE_FILE="$BASE_FIRMWARE_DIR/esp32-v$MICROPYTHON_VERSION.bin"
fi

if [ ! -f "$BASE_FIRMWARE_FILE" ]; then
    log_info "Downloading base MicroPython firmware..."
    if command -v curl &> /dev/null; then
        curl -L -o "$BASE_FIRMWARE_FILE" "$BASE_FIRMWARE_URL"
    elif command -v wget &> /dev/null; then
        wget -O "$BASE_FIRMWARE_FILE" "$BASE_FIRMWARE_URL"
    else
        log_error "Neither curl nor wget found. Please download base firmware manually."
        exit 1
    fi
fi

# Check if esptool is available for creating combined firmware
if command -v esptool.py &> /dev/null; then
    log_info "Creating combined firmware image..."

    if [ "$TARGET" = "esp8266" ]; then
        # For ESP8266, we create a combined image
        cp "$BASE_FIRMWARE_FILE" "$FIRMWARE_PATH"
        # Note: In a real deployment, you'd use esptool to merge the base firmware with main.mpy
        # For now, we'll just copy the base firmware and provide instructions
        log_warn "Combined firmware creation requires manual flashing. See README.md"
    else
        # For ESP32, we can create a combined image
        cp "$BASE_FIRMWARE_FILE" "$FIRMWARE_PATH"
        log_warn "Combined firmware creation requires manual flashing. See README.md"
    fi
else
    log_warn "esptool.py not found. Skipping combined firmware creation."
    log_warn "You'll need to flash base firmware first, then main.mpy separately."
fi

# Create a simple deployment script
DEPLOY_SCRIPT="$BUILD_DIR/deploy.sh"
cat > "$DEPLOY_SCRIPT" << 'EOF'
#!/bin/bash
# DNS-mixer deployment script

if [ $# -ne 2 ]; then
    echo "Usage: $0 <port> <esp8266|esp32>"
    echo "Example: $0 /dev/ttyUSB0 esp8266"
    exit 1
fi

PORT=$1
TARGET=$2

if [ "$TARGET" = "esp8266" ]; then
    FLASH_SIZE="detect"
    FLASH_MODE="dio"
    FLASH_FREQ="40m"
elif [ "$TARGET" = "esp32" ]; then
    FLASH_SIZE="detect"
    FLASH_MODE="dio"
    FLASH_FREQ="40m"
else
    echo "Invalid target. Use 'esp8266' or 'esp32'"
    exit 1
fi

echo "Flashing base MicroPython firmware..."
esptool.py --chip $TARGET --port $PORT --baud 115200 --before default_reset --after hard_reset write_flash -z --flash_mode $FLASH_MODE --flash_freq $FLASH_FREQ --flash_size $FLASH_SIZE 0x1000 ../firmware/${TARGET}-v1.19.1.bin

echo "Flashing DNS-mixer application..."
if [ "$TARGET" = "esp8266" ]; then
    esptool.py --chip $TARGET --port $PORT --baud 115200 --before default_reset --after hard_reset write_flash -z --flash_mode $FLASH_MODE --flash_freq $FLASH_FREQ --flash_size $FLASH_SIZE 0x100000 main.mpy
else
    esptool.py --chip $TARGET --port $PORT --baud 115200 --before default_reset --after hard_reset write_flash -z --flash_mode $FLASH_MODE --flash_freq $FLASH_FREQ --flash_size $FLASH_SIZE 0x100000 main.mpy
fi

echo "Deployment complete! Reset your ESP device."
EOF

chmod +x "$DEPLOY_SCRIPT"

# Create version info
VERSION_FILE="$BUILD_DIR/version.txt"
cat > "$VERSION_FILE" << EOF
DNS-mixer Build Information
===========================
Target: $TARGET
Build Date: $(date)
MicroPython Version: $MICROPYTHON_VERSION
Source: $(basename "$SOURCE_FILE")
Compiled: main.mpy
EOF

log_info "Build completed successfully!"
log_info "Output files:"
log_info "  - $BUILD_DIR/main.mpy (compiled bytecode)"
log_info "  - $BUILD_DIR/$FIRMWARE_NAME (firmware image)"
log_info "  - $BUILD_DIR/deploy.sh (deployment script)"
log_info "  - $BUILD_DIR/version.txt (build info)"
log_info ""
log_info "To flash to your device:"
log_info "  1. Connect your ESP device"
log_info "  2. Run: cd build && ./deploy.sh /dev/ttyUSB0 $TARGET"
