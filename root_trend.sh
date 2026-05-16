#!/bin/bash

# Samsung Galaxy Trend (GT-S7560) Rooting Guide Script
# Method: Heimdall + Custom Recovery + SuperSU

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Galaxy Trend (S7560) Rooting Assistant ===${NC}"
echo "This is an legacy device. We will use Heimdall to flash recovery."
echo ""

# 1. Dependency Check
echo -e "${GREEN}[1/4] Checking Dependencies...${NC}"
if ! command -v heimdall &> /dev/null; then
    echo -e "${RED}Heimdall not found.${NC} Install it with: sudo apt install heimdall-flash"
    exit 1
else
    echo "Heimdall is installed."
fi

# 2. Download Mode
echo ""
echo -e "${GREEN}[2/4] Enter Download Mode${NC}"
echo "1. Power off the phone."
echo "2. Press and hold: ${YELLOW}Volume Down + Home + Power${NC} simultaneously."
echo "3. When the warning appears, press ${YELLOW}Volume Up${NC} to continue."
echo "4. Connect the phone to this PC via USB."

# 3. Flash Recovery
echo ""
echo -e "${GREEN}[3/4] Flashing Custom Recovery (CWM/TWRP)${NC}"
echo "You need a recovery.img (usually CWM for this model)."
echo "Command to flash:"
echo -e "${YELLOW}  sudo heimdall flash --RECOVERY recovery.img --no-reboot${NC}"
echo ""
echo "Note: If the flash fails, you may need to run 'heimdall print-pit' first to initialize connection."

# 4. Final Rooting
echo ""
echo -e "${GREEN}[4/4] Flashing SuperSU${NC}"
echo "1. Once flashed, pull the battery and reinsert it."
echo "2. Boot to Recovery: ${YELLOW}Volume Up + Home + Power${NC}."
echo "3. Use 'Install zip from sdcard'."
echo "4. Choose ${YELLOW}UPDATE-SuperSU-v2.46.zip${NC} (Legacy version for Android 4.0)."
echo "5. Reboot and you are rooted."

echo ""
echo -e "${RED}WARNING: This device is old. Magisk is likely NOT compatible. Use SuperSU 2.46.${NC}"
