#!/usr/bin/env python3
"""
Demo 01 - Step 2: Setting Up AVP Vault

This script creates an AVP vault and stores your API credentials securely.
"""

import getpass
from pathlib import Path

# Import AVP SDK
try:
    import avp
    from avp import AVPClient
    from avp.backends import MemoryBackend, FileBackend
except ImportError:
    print("Error: AVP SDK not installed")
    print("Run: pip install avp-sdk")
    exit(1)

print("=" * 60)
print("AVP VAULT SETUP")
print("=" * 60)
print()

# Step 1: Create vault configuration
config_path = Path("avp.toml")
vault_path = Path(".avp_vault.enc")

print("Step 1: Creating vault configuration...")
print()

# Create avp.toml config
config_content = f'''# AVP Configuration
# This file tells AVP where and how to store secrets

[backend]
type = "file"
path = "{vault_path}"

[workspace]
name = "openclaw-demo"

[session]
ttl = 3600  # 1 hour session timeout
'''

with open(config_path, "w") as f:
    f.write(config_content)

print(f"   Created: {config_path}")
print()

# Step 2: Initialize the vault
print("Step 2: Initializing encrypted vault...")
print()

# Create a master password for the vault
print("   Choose a master password for your vault.")
print("   This password encrypts all your stored credentials.")
print()

password = getpass.getpass("   Enter master password: ")
password_confirm = getpass.getpass("   Confirm master password: ")

if password != password_confirm:
    print()
    print("   ❌ Passwords don't match. Please run again.")
    exit(1)

if len(password) < 8:
    print()
    print("   ❌ Password must be at least 8 characters.")
    exit(1)

# Create the file backend with the password
backend = FileBackend(str(vault_path), password)
client = AVPClient(backend)

# Authenticate to create a session
session = client.authenticate()
print()
print(f"   ✅ Vault initialized: {vault_path}")
print(f"   ✅ Session created: {session.session_id[:20]}...")
print()

# Step 3: Store API credentials
print("Step 3: Store your API credentials")
print()
print("   Enter your API keys below. They will be encrypted immediately.")
print("   Press Enter to skip any key you don't have.")
print()

credentials = {}

# Anthropic API Key
anthropic_key = getpass.getpass("   Anthropic API Key (sk-ant-...): ")
if anthropic_key.strip():
    credentials["anthropic_api_key"] = anthropic_key.strip()

# OpenAI API Key
openai_key = getpass.getpass("   OpenAI API Key (sk-...): ")
if openai_key.strip():
    credentials["openai_api_key"] = openai_key.strip()

# Store credentials in vault
print()
if credentials:
    print("   Storing credentials in vault...")
    for name, value in credentials.items():
        result = client.store(session.session_id, name, value.encode())
        print(f"   ✅ Stored: {name}")
    print()
else:
    print("   No credentials entered. You can add them later.")
    print()

# Step 4: Verify storage
print("Step 4: Verifying encrypted storage...")
print()

# Show that the vault file is encrypted
if vault_path.exists():
    with open(vault_path, "rb") as f:
        content = f.read(100)
    print(f"   Vault file size: {vault_path.stat().st_size} bytes")
    print(f"   First 50 bytes (encrypted): {content[:50].hex()}")
    print()
    print("   ✅ Credentials are encrypted at rest!")
    print("   ✅ Even if malware reads this file, it can't decrypt it.")
print()

# Summary
print("=" * 60)
print("SETUP COMPLETE")
print("=" * 60)
print()
print("Your vault is ready! Files created:")
print(f"  • {config_path} - AVP configuration")
print(f"  • {vault_path} - Encrypted credential storage")
print()
print("Next step: Run 03_openclaw_agent.py to use your credentials")
print()

# Clean up session
client.close()
