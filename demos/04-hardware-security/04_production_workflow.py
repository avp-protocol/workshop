#!/usr/bin/env python3
"""
Demo 04 - Step 4: Production Workflow

Best practices for using hardware security in production AI agents.
"""

import getpass
import time

from avp_hardware import NexusClaw

print("=" * 70)
print("PRODUCTION HARDWARE SECURITY WORKFLOW")
print("=" * 70)
print()

# Connect and authenticate
device = NexusClaw(simulation=True)
device.connect()

if device.is_simulation:
    print("⚠️  Simulation mode - patterns apply to real hardware too")
    print()

pin = getpass.getpass("Enter device PIN: ")
if not device.authenticate(pin):
    print("❌ Authentication failed")
    exit(1)

print("✅ Authenticated")
print()

# Ensure we have a test credential
if "production_api_key" not in device.list():
    device.store("production_api_key", "sk-prod-demo-key-12345")

print("=" * 70)
print("PATTERN 1: MINIMAL EXPOSURE TIME")
print("=" * 70)
print()
print("Retrieve credentials only when needed, use immediately, clear.")
print()

code_example = '''
# GOOD: Minimal exposure
def call_api():
    # Retrieve right before use
    api_key = device.retrieve("production_api_key")

    # Use immediately
    response = make_api_call(api_key)

    # Clear from memory (Python doesn't guarantee this, but helps)
    api_key = None

    return response

# BAD: Long exposure
api_key = device.retrieve("production_api_key")  # Retrieved at startup
# ... hours later ...
response = make_api_call(api_key)  # Key in memory the whole time
'''

print(code_example)
print()

# Demonstrate
print("Demonstrating minimal exposure...")
print()

# Retrieve, use, clear
print("  1. Retrieving credential...")
api_key = device.retrieve("production_api_key")

print("  2. Using credential (simulated API call)...")
time.sleep(0.5)
result = f"API call with {api_key[:10]}... successful"

print("  3. Clearing credential from memory...")
api_key = None

print(f"  4. Result: {result}")
print()

print("=" * 70)
print("PATTERN 2: GRACEFUL HARDWARE UNAVAILABILITY")
print("=" * 70)
print()
print("Handle cases where hardware device is disconnected.")
print()

code_example = '''
def get_credential_with_fallback(name):
    """Try hardware first, fall back to encrypted file."""
    try:
        # Try hardware (most secure)
        return hardware_device.retrieve(name)
    except DeviceNotConnectedError:
        logger.warning("Hardware not available, using file backend")
        # Fall back to encrypted file (less secure but available)
        return file_backend.retrieve(name)
    except Exception as e:
        logger.error(f"All backends failed: {e}")
        raise
'''

print(code_example)
print()

print("=" * 70)
print("PATTERN 3: STARTUP VALIDATION")
print("=" * 70)
print()
print("Validate hardware and credentials at startup, fail fast.")
print()

code_example = '''
def startup_validation():
    """Validate hardware security at application startup."""

    # 1. Check device connected
    if not device.is_connected():
        raise StartupError("NexusClaw not connected")

    # 2. Verify device integrity
    info = device.get_info()
    if info.tamper_detected:
        raise SecurityError("Tamper detected! Do not proceed.")

    # 3. Verify required credentials exist
    required = ["anthropic_api_key", "database_password"]
    available = device.list()

    missing = set(required) - set(available)
    if missing:
        raise StartupError(f"Missing credentials: {missing}")

    # 4. Test retrieval works (touch confirmation)
    print("Touch device to confirm startup...")
    device.retrieve(required[0])

    print("✅ Hardware security validated")
'''

print(code_example)
print()

print("=" * 70)
print("PATTERN 4: CREDENTIAL ROTATION")
print("=" * 70)
print()
print("Rotate credentials with zero downtime.")
print()

code_example = '''
def rotate_credential(name, new_value):
    """Rotate a credential in hardware with audit logging."""

    # 1. Store new credential with temporary name
    temp_name = f"{name}_new"
    device.store(temp_name, new_value)

    # 2. Verify new credential works
    test_value = device.retrieve(temp_name)
    if not verify_credential_works(test_value):
        device.delete(temp_name)
        raise RotationError("New credential validation failed")

    # 3. Delete old credential
    device.delete(name)

    # 4. Rename new to original name
    device.store(name, new_value)
    device.delete(temp_name)

    # 5. Audit log
    logger.info(f"Credential rotated: {name}")
'''

print(code_example)
print()

print("=" * 70)
print("PATTERN 5: MULTI-DEVICE SETUP")
print("=" * 70)
print()
print("For high-availability, use multiple hardware keys.")
print()

code_example = '''
class HACredentialManager:
    """High-availability credential manager with multiple devices."""

    def __init__(self, devices: list[NexusClaw]):
        self.devices = devices

    def retrieve(self, name):
        """Try each device until one succeeds."""
        errors = []

        for device in self.devices:
            try:
                return device.retrieve(name)
            except Exception as e:
                errors.append((device, e))

        raise AllDevicesFailedError(errors)

    def store(self, name, value):
        """Store to ALL devices for redundancy."""
        for device in self.devices:
            device.store(name, value)

# Usage: 2 NexusClaw devices for redundancy
manager = HACredentialManager([
    NexusClaw("/dev/ttyUSB0"),  # Primary
    NexusClaw("/dev/ttyUSB1"),  # Backup
])
'''

print(code_example)
print()

print("=" * 70)
print("WORKSHOP COMPLETE!")
print("=" * 70)
print()
print("You've learned:")
print()
print("  ✅ Demo 01: Basic AVP credential storage")
print("  ✅ Demo 02: LangChain integration")
print("  ✅ Demo 03: Multi-agent credential management")
print("  ✅ Demo 04: Hardware security for maximum protection")
print()
print("Next steps:")
print()
print("  1. Get a NexusClaw device for production use")
print("  2. Migrate your existing credentials to AVP")
print("  3. Implement the production patterns shown above")
print("  4. Set up credential rotation policies")
print()
print("Resources:")
print("  • AVP Specification: https://github.com/avp-protocol/spec")
print("  • NexusClaw: https://github.com/avp-protocol/nexusclaw")
print("  • AVP Python SDK: https://pypi.org/project/avp-sdk/")
print()

device.disconnect()
