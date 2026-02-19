#!/usr/bin/env python3
"""
Demo 01 - Step 3: Using AVP with an AI Agent

This script demonstrates how to securely retrieve credentials from AVP
and use them with an AI agent (using Anthropic's Claude as an example).
"""

import getpass
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

# Import Anthropic SDK (optional - for demo purposes)
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

print("=" * 60)
print("SECURE AI AGENT WITH AVP")
print("=" * 60)
print()

# Check vault exists
vault_path = Path(".avp_vault.enc")
if not vault_path.exists():
    print("❌ Vault not found. Run 02_setup_vault.py first.")
    exit(1)

# Step 1: Authenticate with AVP
print("Step 1: Unlocking AVP vault...")
print()

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

# Step 2: Retrieve API credentials
print("Step 2: Retrieving credentials from vault...")
print()

try:
    result = client.retrieve(session.session_id, "anthropic_api_key")
    api_key = result.value.decode()
    print(f"   ✅ Retrieved: anthropic_api_key")
    print(f"   ✅ Key preview: {api_key[:15]}...{api_key[-4:]}")
    print()
except Exception as e:
    print(f"   ❌ No Anthropic API key found in vault")
    print(f"   Run 02_setup_vault.py to add credentials")
    client.close()
    exit(1)

# Step 3: Use with AI agent
print("Step 3: Using credentials with AI agent...")
print()

if HAS_ANTHROPIC:
    print("   Creating Anthropic client with AVP credentials...")

    # Create the Anthropic client with the retrieved key
    anthropic_client = anthropic.Anthropic(api_key=api_key)

    # Make a simple API call
    print("   Sending test message to Claude...")
    print()

    try:
        message = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'AVP credentials working!' in exactly 5 words."}
            ]
        )

        response = message.content[0].text
        print("   " + "=" * 50)
        print(f"   Claude says: {response}")
        print("   " + "=" * 50)
        print()
        print("   ✅ API call successful! Credentials working.")

    except anthropic.AuthenticationError:
        print("   ❌ Authentication failed - API key may be invalid")
    except Exception as e:
        print(f"   ❌ API call failed: {e}")
else:
    print("   Anthropic SDK not installed (pip install anthropic)")
    print("   Simulating credential usage...")
    print()
    print("   In a real application, you would do:")
    print()
    print("   ```python")
    print("   import anthropic")
    print("   client = anthropic.Anthropic(api_key=api_key)")
    print("   response = client.messages.create(...)")
    print("   ```")
    print()
    print("   ✅ Credentials retrieved successfully!")

print()

# Step 4: Security summary
print("=" * 60)
print("SECURITY BENEFITS")
print("=" * 60)
print()
print("What we achieved:")
print()
print("  1. API key stored encrypted at rest")
print("     - File on disk is unreadable without password")
print("     - Malware can't steal plaintext credentials")
print()
print("  2. No credentials in environment variables")
print("     - Not visible in `ps aux`")
print("     - Not leaked to child processes")
print()
print("  3. No credentials in source code")
print("     - Safe to commit this script to git")
print("     - No secrets in version history")
print()
print("  4. Session-based access")
print("     - Credentials only accessible during session")
print("     - Session expires after TTL")
print()

# Cleanup
client.close()
print("Done! Session closed.")
