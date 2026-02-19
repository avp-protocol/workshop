#!/usr/bin/env python3
"""
Demo 02 - Step 4: Multi-Provider Credential Management

Shows how to manage credentials for multiple AI providers with AVP.
"""

from pathlib import Path

if not Path(".avp_vault.enc").exists():
    print("❌ Vault not found. Run 01_setup_credentials.py first.")
    exit(1)

print("=" * 60)
print("MULTI-PROVIDER CREDENTIAL MANAGEMENT")
print("=" * 60)
print()

from avp_langchain import AVPCredentialProvider

# Load credentials
print("Loading credentials from AVP vault...")
credentials = AVPCredentialProvider(".avp_vault.enc", workspace="langchain")
available = credentials.list()
print(f"✅ Found credentials: {', '.join(available)}")
print()

# Provider configurations
providers = {}

print("Configuring available providers...")
print()

# Anthropic
if "anthropic_api_key" in available:
    try:
        from langchain_anthropic import ChatAnthropic
        providers["anthropic"] = {
            "name": "Anthropic Claude",
            "llm": ChatAnthropic(
                model="claude-3-haiku-20240307",
                api_key=credentials.get("anthropic_api_key"),
                max_tokens=100
            )
        }
        print("  ✅ Anthropic Claude configured")
    except ImportError:
        print("  ⚠️  langchain-anthropic not installed")

# OpenAI
if "openai_api_key" in available:
    try:
        from langchain_openai import ChatOpenAI
        providers["openai"] = {
            "name": "OpenAI GPT",
            "llm": ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=credentials.get("openai_api_key"),
                max_tokens=100
            )
        }
        print("  ✅ OpenAI GPT configured")
    except ImportError:
        print("  ⚠️  langchain-openai not installed")

if not providers:
    print()
    print("❌ No providers available. Add API keys with 01_setup_credentials.py")
    credentials.close()
    exit(1)

print()
print(f"Available providers: {', '.join(providers.keys())}")
print()

# Compare responses
print("=" * 60)
print("COMPARING PROVIDER RESPONSES")
print("=" * 60)
print()

test_prompt = "In exactly 10 words, what makes a good AI assistant?"
print(f"Prompt: '{test_prompt}'")
print()

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("user", "{input}")
])

for provider_id, config in providers.items():
    print(f"{config['name']}:")
    try:
        chain = prompt | config["llm"]
        response = chain.invoke({"input": test_prompt})
        print(f"  → {response.content}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()

# Demonstrate credential rotation
print("=" * 60)
print("CREDENTIAL MANAGEMENT FEATURES")
print("=" * 60)
print()

print("AVP provides these credential management capabilities:")
print()
print("  1. LIST - View all stored credentials")
print(f"     credentials.list() → {available}")
print()
print("  2. GET - Retrieve a specific credential")
print("     credentials.get('anthropic_api_key') → sk-ant-...****")
print()
print("  3. SET - Store a new credential")
print("     credentials.set('new_key', 'value')")
print()
print("  4. ROTATE - Update with version tracking")
print("     credentials.rotate('api_key', 'new_value')")
print()
print("  5. DELETE - Remove a credential")
print("     credentials.delete('old_key')")
print()

# Example: Add a new provider credential
print("=" * 60)
print("TRY IT: ADD A NEW CREDENTIAL")
print("=" * 60)
print()

import getpass

add_new = input("Add a new credential? (yes/no): ")
if add_new.lower() == "yes":
    name = input("Credential name (e.g., 'cohere_api_key'): ").strip()
    if name:
        value = getpass.getpass(f"Value for '{name}': ")
        if value:
            credentials.set(name, value)
            print(f"✅ Stored: {name}")
            print(f"   Current credentials: {credentials.list()}")
        else:
            print("Skipped (no value entered)")
    else:
        print("Skipped (no name entered)")

print()
print("Session complete. All credentials remain encrypted at rest.")
credentials.close()
