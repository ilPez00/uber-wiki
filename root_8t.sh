#!/bin/bash

# OnePlus 8T (KB2003/KB2001/KB2005) Rooting Guide Script
# Target: OxygenOS (Android 11-14) via Magisk

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== OnePlus 8T Rooting Assistant ===${NC}"
echo "This script provides instructions and checks for rooting your device."
echo -e "${RED}WARNING: UNLOCKING BOOTLOADER WIPES ALL DATA. PROCEED WITH CAUTION.${NC}"
echo ""

# 1. Connectivity Check
echo -e "${GREEN}[1/4] Checking ADB Connection...${NC}"
DEVICE_ID=$(adb devices | grep -v "List" | grep "device" | awk '{print $1}')

if [ -z "$DEVICE_ID" ]; then
    echo -e "${RED}Error: No device detected via ADB.${NC}"
    echo "Ensure:"
    echo "  - USB Debugging is ON (Settings > Developer Options)"
    echo "  - Cable is connected and 'Allow USB Debugging' is checked on phone"
    exit 1
else
    echo -e "${GREEN}Device detected: $DEVICE_ID${NC}"
fi

# 2. Bootloader Status
echo ""
echo -e "${GREEN}[2/4] Bootloader & OEM Unlock Instructions${NC}"
echo "1. Go to Settings > About Phone > Tap 'Build Number' 7 times."
echo "2. Go to Settings > System > Developer Options."
echo "3. Enable 'OEM Unlocking' and 'USB Debugging'."
echo "4. Run: ${YELLOW}adb reboot bootloader${NC}"
echo "5. Once in fastboot mode, run: ${YELLOW}fastboot oem unlock${NC}"
echo "6. Select 'UNLOCK THE BOOTLOADER' using volume keys and power to confirm."
echo -e "${RED}NOTE: Your phone will factory reset now.${NC}"

# 3. Getting the Boot Image
echo ""
echo -e "${GREEN}[3/4] Magisk Patching Phase${NC}"
echo "To root, we need your current 'boot.img'."
echo "1. Download the full OxygenOS ZIP for your EXACT version (Settings > About)."
echo "2. Use 'payload-dumper-go' (or ask me) to extract 'boot.img' from the ZIP."
echo "3. Copy 'boot.img' to your phone: ${YELLOW}adb push boot.img /sdcard/Download/${NC}"
echo "4. Install Magisk App on your phone."
echo "5. Open Magisk > Install > Select and Patch a File > Pick 'boot.img'."
echo "6. Copy patched file back: ${YELLOW}adb pull /sdcard/Download/magisk_patched_xxx.img .${NC}"

# 4. Flashing
echo ""
echo -e "${GREEN}[4/4] Final Flash Instructions${NC}"
echo "1. Reboot to fastboot: ${YELLOW}adb reboot bootloader${NC}"
echo "2. Verify fastboot: ${YELLOW}fastboot devices${NC}"
echo "3. Flash the patched boot: ${YELLOW}fastboot flash boot magisk_patched_xxx.img${NC}"
echo "4. Reboot: ${YELLOW}fastboot reboot${NC}"
echo ""
echo -e "${GREEN}Rooting complete once phone reboots. Open Magisk to verify!${NC}"
