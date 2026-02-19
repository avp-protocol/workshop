#!/usr/bin/env python3
"""
Demo 01 - Step 1: The Insecure Approach (DON'T DO THIS IN PRODUCTION!)

This script demonstrates common insecure patterns for storing API credentials.
We show these patterns to highlight what AVP helps you avoid.
"""

import os
import json
from pathlib import Path

print("=" * 60)
print("INSECURE CREDENTIAL STORAGE PATTERNS")
print("=" * 60)
print()
print("These are common but DANGEROUS ways to store API keys:")
print()

# Pattern 1: Environment Variables
print("1. ENVIRONMENT VARIABLES")
print("-" * 40)
api_key = os.environ.get("ANTHROPIC_API_KEY", "not-set")
if api_key != "not-set":
    print(f"   Found key in env: {api_key[:20]}...")
    print("   ❌ Risk: Visible in `ps aux -e`, process dumps, shell history")
else:
    print("   No key found in environment")
    print("   ❌ Risk: If set, visible in `ps aux -e`, process dumps")
print()

# Pattern 2: .env file
print("2. PLAINTEXT .env FILE")
print("-" * 40)
env_file = Path(".env")
if env_file.exists():
    print(f"   Found .env file with {len(env_file.read_text())} bytes")
    print("   ❌ Risk: Stolen by malware, accidentally committed to git")
else:
    print("   No .env file found")
    print("   ❌ Risk: If created, easily stolen by infostealer malware")
print()

# Pattern 3: keys.json
print("3. PLAINTEXT keys.json")
print("-" * 40)
keys_file = Path("keys.json")
if keys_file.exists():
    with open(keys_file) as f:
        keys = json.load(f)
    print(f"   Found keys.json with {len(keys)} keys")
    print("   ❌ Risk: Stolen by malware, accidentally committed to git")
else:
    print("   No keys.json found")
    print("   ❌ Risk: If created, plaintext on disk = easy target")
print()

# Pattern 4: Hardcoded
print("4. HARDCODED IN SOURCE CODE")
print("-" * 40)
print('   api_key = "sk-ant-api03-xxxxx"  # NEVER DO THIS!')
print("   ❌ Risk: Committed to git, visible in source control history forever")
print()

# Summary
print("=" * 60)
print("WHY THESE PATTERNS ARE DANGEROUS")
print("=" * 60)
print()
print("Infostealer malware specifically targets:")
print("  • .env files")
print("  • keys.json, credentials.json")
print("  • Browser password stores")
print("  • SSH keys")
print()
print("Once stolen, attackers can:")
print("  • Make API calls on your account")
print("  • Access your AI agent's capabilities")
print("  • Rack up thousands in API charges")
print("  • Exfiltrate data through your agents")
print()
print("=" * 60)
print("THE SOLUTION: AVP")
print("=" * 60)
print()
print("AVP stores credentials encrypted at rest.")
print("Even if malware reads the vault file, it can't decrypt it")
print("without the master key (which can be in OS keychain or hardware).")
print()
print("Next step: Run 02_setup_vault.py to set up AVP")
print()
