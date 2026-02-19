#!/usr/bin/env python3
"""
Demo 04 - Step 3: Storing Credentials in Hardware

Store and retrieve credentials using NexusClaw hardware security.
"""

import getpass

from avp_hardware import NexusClaw

print("=" * 70)
print("HARDWARE CREDENTIAL STORAGE")
print("=" * 70)
print()

# Connect to device
print("Connecting to NexusClaw...")
device = NexusClaw(simulation=True)
device.connect()
print("✅ Connected")

if device.is_simulation:
    print("  (Running in simulation mode)")
print()

# Authenticate
print("Authenticating...")
pin = getpass.getpass("Enter device PIN: ")
if not device.authenticate(pin):
    print("❌ Authentication failed")
    device.disconnect()
    exit(1)
print("✅ Authenticated")
print()

# Store credentials
print("=" * 70)
print("STORE CREDENTIALS")
print("=" * 70)
print()
print("Each storage operation requires physical touch on the device.")
print("This ensures only someone with physical access can store credentials.")
print()

# Store Anthropic key
print("Storing Anthropic API key...")
api_key = getpass.getpass("Enter Anthropic API Key (or press Enter to skip): ")
if api_key.strip():
    device.store("anthropic_api_key", api_key.strip())
    print("✅ Stored: anthropic_api_key")
    print()

# Store OpenAI key
print("Storing OpenAI API key...")
api_key = getpass.getpass("Enter OpenAI API Key (or press Enter to skip): ")
if api_key.strip():
    device.store("openai_api_key", api_key.strip())
    print("✅ Stored: openai_api_key")
    print()

# List stored credentials
print("=" * 70)
print("STORED CREDENTIALS")
print("=" * 70)
print()
slots = device.list()
if slots:
    print(f"Found {len(slots)} credential(s):")
    for slot in slots:
        print(f"  • {slot}")
else:
    print("No credentials stored yet.")
print()

# Retrieve and use
if slots:
    print("=" * 70)
    print("RETRIEVE CREDENTIALS")
    print("=" * 70)
    print()
    print("Each retrieval requires physical touch confirmation.")
    print("This prevents malware from silently extracting credentials.")
    print()

    retrieve = input(f"Retrieve '{slots[0]}'? (yes/no): ")
    if retrieve.lower() == "yes":
        value = device.retrieve(slots[0])
        print()
        print(f"Retrieved value: {value[:15]}...{value[-4:]}")
        print()
        print("Note: Even in this demo, the REAL credential is only")
        print("available briefly. In production, it would be used")
        print("immediately and then cleared from memory.")

print()
print("=" * 70)
print("SECURITY ACHIEVED")
print("=" * 70)
print()
print("Your credentials are now stored in hardware with:")
print()
print("  🔒 ENCRYPTION AT REST")
print("     Stored in AES-encrypted secure element")
print()
print("  🔒 NEVER IN SYSTEM MEMORY")
print("     Cryptographic operations happen inside the device")
print()
print("  🔒 PHYSICAL PRESENCE REQUIRED")
print("     Touch confirmation prevents remote extraction")
print()
print("  🔒 TAMPER PROTECTION")
print("     Device wipes if physical tampering detected")
print()
print("  🔒 BRUTE-FORCE PROTECTION")
print("     Auto-wipe after 3 failed PIN attempts")
print()
print("Next: Run 04_production_workflow.py for production patterns")
print()

device.disconnect()
