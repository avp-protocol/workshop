#!/usr/bin/env python3
"""
Demo 04 - Step 2: Setting Up NexusClaw

Initialize and configure a NexusClaw hardware security key.
(Uses simulation mode if no physical device is available)
"""

import getpass

from avp_hardware import NexusClaw, SecurityLevel

print("=" * 70)
print("NEXUSCLAW SETUP")
print("=" * 70)
print()

# Initialize device (auto-detects simulation mode)
print("Initializing NexusClaw...")
device = NexusClaw(simulation=True)  # Force simulation for demo

if device.is_simulation:
    print()
    print("  ⚠️  SIMULATION MODE")
    print("  No physical NexusClaw detected. Using simulated device.")
    print("  This demonstrates the workflow without real hardware.")
    print()
    print("  To use real hardware:")
    print("  1. Connect NexusClaw USB device")
    print("  2. Run this script again")
    print()

# Connect to device
print("Connecting to device...")
device.connect()
print("✅ Connected")
print()

# Get device info
print("Device Information:")
print("-" * 40)
info = device.get_info()
print(f"  Device ID:        {info.device_id}")
print(f"  Firmware:         {info.firmware_version}")
print(f"  Secure Element:   {info.secure_element}")
print(f"  Slots:            {info.slots_used}/{info.slots_total}")
print(f"  Tamper Detected:  {'⚠️ YES' if info.tamper_detected else '✅ No'}")
print()

# Set up PIN
print("=" * 70)
print("PIN SETUP")
print("=" * 70)
print()
print("The device PIN protects against unauthorized access.")
print("After 3 failed attempts, the device will WIPE all stored credentials.")
print()

while True:
    pin = getpass.getpass("Choose a PIN (4+ digits): ")
    if len(pin) < 4:
        print("PIN must be at least 4 digits. Try again.")
        continue

    pin_confirm = getpass.getpass("Confirm PIN: ")
    if pin != pin_confirm:
        print("PINs don't match. Try again.")
        continue

    break

print()
print("Setting up PIN...")
device.setup(pin)
print("✅ PIN configured")
print()

# Authenticate
print("Testing authentication...")
device.authenticate(pin)
print("✅ Authentication successful")
print()

# Summary
print("=" * 70)
print("SETUP COMPLETE")
print("=" * 70)
print()
print("Your NexusClaw is ready to store credentials.")
print()
print("Security features enabled:")
print("  ✅ Tamper-resistant secure element")
print("  ✅ PIN protection")
print("  ✅ Auto-wipe after failed attempts")
print("  ✅ Touch confirmation for operations")
print()
print("Next: Run 03_hardware_storage.py to store credentials")
print()

device.disconnect()
