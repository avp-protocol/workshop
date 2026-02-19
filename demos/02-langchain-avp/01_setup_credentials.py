#!/usr/bin/env python3
"""
Demo 02 - Step 1: Set up credentials for LangChain

Creates an AVP vault with credentials needed for LangChain examples.
"""

import getpass
from pathlib import Path

from avp import AVPClient
from avp.backends import FileBackend

print("=" * 60)
print("LANGCHAIN + AVP CREDENTIAL SETUP")
print("=" * 60)
print()

vault_path = Path(".avp_vault.enc")

# Check if vault already exists
if vault_path.exists():
    print(f"Vault already exists: {vault_path}")
    print()
    update = input("Add/update credentials? (yes/no): ")
    if update.lower() != "yes":
        print("Setup cancelled.")
        exit(0)
    print()
    password = getpass.getpass("Enter existing vault password: ")
else:
    print("Creating new vault...")
    print()
    password = getpass.getpass("Choose vault password: ")
    password_confirm = getpass.getpass("Confirm password: ")
    if password != password_confirm:
        print("Passwords don't match!")
        exit(1)

# Connect to vault
print()
print("Connecting to vault...")
backend = FileBackend(str(vault_path), password)
client = AVPClient(backend)
session = client.authenticate(workspace="langchain")
print("✅ Connected")
print()

# Collect credentials
print("Enter your API credentials (press Enter to skip):")
print()

credentials = {}

# Anthropic
key = getpass.getpass("Anthropic API Key (sk-ant-...): ")
if key.strip():
    credentials["anthropic_api_key"] = key.strip()

# OpenAI
key = getpass.getpass("OpenAI API Key (sk-...): ")
if key.strip():
    credentials["openai_api_key"] = key.strip()

# Store credentials
print()
if credentials:
    print("Storing credentials...")
    for name, value in credentials.items():
        client.store(session.session_id, name, value.encode())
        print(f"  ✅ {name}")
else:
    print("No credentials entered.")

print()
print("=" * 60)
print("SETUP COMPLETE")
print("=" * 60)
print()
print("Your credentials are securely stored in AVP.")
print()
print("Next: Run 02_basic_chain.py to test LangChain integration")
print()

client.close()
