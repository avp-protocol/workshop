"""
AVP Hardware Backend Wrapper

Provides a high-level interface for NexusClaw hardware security keys.
Includes simulation mode for learning without physical hardware.
"""

import getpass
import time
from typing import Optional
from dataclasses import dataclass
from enum import Enum

# Try to import actual hardware backend
try:
    from avp.backends import HardwareBackend
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False


class SecurityLevel(Enum):
    """Security levels for credential storage."""
    PLAINTEXT = 1
    ENCRYPTED_FILE = 2
    OS_KEYCHAIN = 3
    HARDWARE = 4


@dataclass
class HardwareInfo:
    """Information about connected hardware device."""
    device_id: str
    firmware_version: str
    secure_element: str
    slots_used: int
    slots_total: int
    tamper_detected: bool


class NexusClawSimulator:
    """
    Simulates NexusClaw hardware for learning purposes.

    This allows you to understand the hardware workflow without
    having physical hardware. In simulation mode, credentials
    are stored in memory (NOT secure - only for demos).
    """

    def __init__(self):
        self._connected = False
        self._pin_set = False
        self._pin: Optional[str] = None
        self._slots: dict = {}
        self._max_slots = 32
        self._failed_attempts = 0
        self._max_attempts = 3

    def connect(self) -> bool:
        """Simulate connecting to device."""
        print("  [SIM] Searching for NexusClaw device...")
        time.sleep(0.5)
        print("  [SIM] Found simulated device on /dev/ttyUSB0")
        self._connected = True
        return True

    def get_info(self) -> HardwareInfo:
        """Get simulated device info."""
        return HardwareInfo(
            device_id="NXCLAW-SIM-0001",
            firmware_version="1.0.0-sim",
            secure_element="TROPIC01-SIM",
            slots_used=len(self._slots),
            slots_total=self._max_slots,
            tamper_detected=False
        )

    def setup_pin(self, pin: str) -> bool:
        """Set up device PIN."""
        if len(pin) < 4:
            raise ValueError("PIN must be at least 4 digits")
        self._pin = pin
        self._pin_set = True
        print("  [SIM] PIN configured successfully")
        return True

    def verify_pin(self, pin: str) -> bool:
        """Verify device PIN."""
        if pin == self._pin:
            self._failed_attempts = 0
            return True
        else:
            self._failed_attempts += 1
            if self._failed_attempts >= self._max_attempts:
                print("  [SIM] ⚠️  MAX ATTEMPTS REACHED - Device would wipe!")
                self._slots = {}
            return False

    def store(self, slot_name: str, value: bytes) -> bool:
        """Store credential in simulated secure element."""
        if len(self._slots) >= self._max_slots:
            raise ValueError("No free slots available")

        print(f"  [SIM] Touch the device to confirm storage...")
        time.sleep(1)
        print(f"  [SIM] ✓ Touch confirmed")

        self._slots[slot_name] = value
        return True

    def retrieve(self, slot_name: str) -> bytes:
        """Retrieve credential from simulated secure element."""
        if slot_name not in self._slots:
            raise KeyError(f"Slot '{slot_name}' not found")

        print(f"  [SIM] Touch the device to confirm retrieval...")
        time.sleep(1)
        print(f"  [SIM] ✓ Touch confirmed")

        return self._slots[slot_name]

    def delete(self, slot_name: str) -> bool:
        """Delete credential from simulated secure element."""
        if slot_name in self._slots:
            del self._slots[slot_name]
            return True
        return False

    def list_slots(self) -> list:
        """List all used slots."""
        return list(self._slots.keys())

    def disconnect(self):
        """Disconnect from simulated device."""
        self._connected = False


class NexusClaw:
    """
    High-level interface for NexusClaw hardware security key.

    Automatically uses simulation mode if hardware is not available.
    """

    def __init__(self, device_path: Optional[str] = None, simulation: bool = False):
        """
        Initialize NexusClaw interface.

        Args:
            device_path: Path to USB device (e.g., /dev/ttyUSB0)
            simulation: Force simulation mode even if hardware available
        """
        self._simulation = simulation or not HAS_HARDWARE
        self._device: Optional[any] = None
        self._authenticated = False

        if self._simulation:
            self._device = NexusClawSimulator()
        else:
            # Real hardware initialization would go here
            raise NotImplementedError("Real hardware support coming soon")

    @property
    def is_simulation(self) -> bool:
        """Check if running in simulation mode."""
        return self._simulation

    def connect(self) -> bool:
        """Connect to the hardware device."""
        return self._device.connect()

    def get_info(self) -> HardwareInfo:
        """Get device information."""
        return self._device.get_info()

    def setup(self, pin: str) -> bool:
        """
        Initial device setup with PIN.

        Args:
            pin: 4+ digit PIN for device access
        """
        return self._device.setup_pin(pin)

    def authenticate(self, pin: str) -> bool:
        """
        Authenticate with device PIN.

        Args:
            pin: Device PIN

        Returns:
            True if authenticated
        """
        if self._device.verify_pin(pin):
            self._authenticated = True
            return True
        return False

    def store(self, name: str, value: str) -> bool:
        """
        Store a credential in the hardware secure element.

        Args:
            name: Credential name
            value: Credential value

        Note: Requires physical touch confirmation on device.
        """
        if not self._authenticated:
            raise PermissionError("Must authenticate with PIN first")
        return self._device.store(name, value.encode())

    def retrieve(self, name: str) -> str:
        """
        Retrieve a credential from the hardware secure element.

        Args:
            name: Credential name

        Returns:
            Credential value

        Note: Requires physical touch confirmation on device.
        """
        if not self._authenticated:
            raise PermissionError("Must authenticate with PIN first")
        return self._device.retrieve(name).decode()

    def delete(self, name: str) -> bool:
        """Delete a credential from the device."""
        if not self._authenticated:
            raise PermissionError("Must authenticate with PIN first")
        return self._device.delete(name)

    def list(self) -> list:
        """List all stored credentials."""
        if not self._authenticated:
            raise PermissionError("Must authenticate with PIN first")
        return self._device.list_slots()

    def disconnect(self):
        """Disconnect from the device."""
        if self._device:
            self._device.disconnect()
        self._authenticated = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False
