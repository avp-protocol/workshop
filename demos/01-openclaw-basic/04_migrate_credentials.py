#!/usr/bin/env python3
"""
Demo 01 - Step 4: Migrate Existing Credentials to AVP

This script helps migrate credentials from insecure storage formats
(keys.json, .env files) to AVP encrypted storage.
"""

import getpass
import json
import os
from pathlib import Path

# Import AVP SDK
try:
    import avp
    from avp import AVPClient
    from avp.backends import FileBackend
except ImportError:
    print("Error: AVP SDK not installed")
    print("Run: pip install avp-sdk")
    exit(1)

print("=" * 60)
print("CREDENTIAL MIGRATION TO AVP")
print("=" * 60)
print()

# Check vault exists
vault_path = Path(".avp_vault.enc")
if not vault_path.exists():
    print("❌ Vault not found. Run 02_setup_vault.py first.")
    exit(1)

# Unlock vault
print("Step 1: Unlocking AVP vault...")
password = getpass.getpass("   Enter vault password: ")

try:
    backend = FileBackend(str(vault_path), password)
    client = AVPClient(backend)
    session = client.authenticate()
    print("   ✅ Vault unlocked")
    print()
except Exception as e:
    print(f"   ❌ Failed to unlock vault: {e}")
    exit(1)

# Find credentials to migrate
print("Step 2: Scanning for credentials to migrate...")
print()

credentials_found = {}

# Check for keys.json
keys_files = ["keys.json", "credentials.json", "secrets.json", ".keys.json"]
for filename in keys_files:
    path = Path(filename)
    if path.exists():
        print(f"   Found: {filename}")
        try:
            with open(path) as f:
                data = json.load(f)
            for key, value in data.items():
                if isinstance(value, str) and len(value) > 10:
                    credentials_found[key] = (value, filename)
                    print(f"      - {key}: {value[:15]}...")
        except Exception as e:
            print(f"      Error reading: {e}")
        print()

# Check for .env file
env_path = Path(".env")
if env_path.exists():
    print(f"   Found: .env")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if "KEY" in key.upper() or "TOKEN" in key.upper() or "SECRET" in key.upper():
                    credentials_found[key.lower()] = (value, ".env")
                    print(f"      - {key}: {value[:15]}...")
    print()

# Check for environment variables
env_vars = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GITHUB_TOKEN", "AWS_SECRET_ACCESS_KEY"]
for var in env_vars:
    value = os.environ.get(var)
    if value:
        credentials_found[var.lower()] = (value, "environment")
        print(f"   Found in environment: {var}")
        print(f"      - {var}: {value[:15]}...")

if not credentials_found:
    print("   No credentials found to migrate.")
    print()
    print("   Supported sources:")
    print("     - keys.json, credentials.json, secrets.json")
    print("     - .env file")
    print("     - Environment variables (ANTHROPIC_API_KEY, etc.)")
    client.close()
    exit(0)

print()
print(f"   Found {len(credentials_found)} credential(s) to migrate")
print()

# Confirm migration
print("Step 3: Migrate credentials to AVP")
print()
confirm = input("   Migrate these credentials to AVP? (yes/no): ")

if confirm.lower() != "yes":
    print("   Migration cancelled.")
    client.close()
    exit(0)

print()
print("   Migrating...")

migrated = 0
for name, (value, source) in credentials_found.items():
    try:
        client.store(session.session_id, name, value.encode())
        print(f"   ✅ {name} (from {source})")
        migrated += 1
    except Exception as e:
        print(f"   ❌ {name}: {e}")

print()
print(f"   Migrated {migrated}/{len(credentials_found)} credentials")
print()

# Offer to delete old files
print("Step 4: Clean up insecure files")
print()
print("   IMPORTANT: Now that credentials are in AVP, you should delete")
print("   the old plaintext files to prevent future theft.")
print()

files_to_delete = set()
for name, (value, source) in credentials_found.items():
    if source not in ["environment"]:
        files_to_delete.add(source)

if files_to_delete:
    print("   Files to delete:")
    for f in files_to_delete:
        print(f"     - {f}")
    print()

    confirm_delete = input("   Delete these files? (yes/no): ")

    if confirm_delete.lower() == "yes":
        for f in files_to_delete:
            try:
                # Overwrite with zeros before deleting (secure delete)
                path = Path(f)
                size = path.stat().st_size
                with open(path, "wb") as file:
                    file.write(b"\x00" * size)
                path.unlink()
                print(f"   ✅ Securely deleted: {f}")
            except Exception as e:
                print(f"   ❌ Could not delete {f}: {e}")
    else:
        print()
        print("   ⚠️  Files not deleted. Remember to delete them manually!")
        print("   Those plaintext files are a security risk.")

print()
print("=" * 60)
print("MIGRATION COMPLETE")
print("=" * 60)
print()
print("Your credentials are now stored in AVP encrypted storage.")
print("Use 03_openclaw_agent.py to see how to retrieve them.")
print()

client.close()
