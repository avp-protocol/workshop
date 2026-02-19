#!/usr/bin/env python3
"""
Demo 02 - Step 2: Basic LangChain with AVP

Shows how to use AVP credentials with a simple LangChain chain.
"""

from pathlib import Path

# Check vault exists
if not Path(".avp_vault.enc").exists():
    print("❌ Vault not found. Run 01_setup_credentials.py first.")
    exit(1)

print("=" * 60)
print("LANGCHAIN + AVP BASIC EXAMPLE")
print("=" * 60)
print()

# Import AVP credential provider
from avp_langchain import AVPCredentialProvider

print("Step 1: Loading credentials from AVP vault...")
print()

try:
    credentials = AVPCredentialProvider(".avp_vault.enc", workspace="langchain")
    print("  ✅ Vault unlocked")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    exit(1)

# Check available credentials
available = credentials.list()
print(f"  ✅ Found {len(available)} credential(s): {', '.join(available)}")
print()

# Try to use LangChain
print("Step 2: Creating LangChain LLM...")
print()

try:
    if "anthropic_api_key" in available:
        from langchain_anthropic import ChatAnthropic

        api_key = credentials.get("anthropic_api_key")
        llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            api_key=api_key,
            max_tokens=100
        )
        provider = "Anthropic Claude"

    elif "openai_api_key" in available:
        from langchain_openai import ChatOpenAI

        api_key = credentials.get("openai_api_key")
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=api_key,
            max_tokens=100
        )
        provider = "OpenAI GPT"

    else:
        print("  ❌ No API keys found in vault")
        print("  Run 01_setup_credentials.py to add credentials")
        credentials.close()
        exit(1)

    print(f"  ✅ Created {provider} LLM")
    print()

except ImportError as e:
    print(f"  ❌ LangChain not installed: {e}")
    print("  Run: pip install langchain-anthropic langchain-openai")
    credentials.close()
    exit(1)

# Run a simple chain
print("Step 3: Running LangChain...")
print()

try:
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Be concise."),
        ("user", "{input}")
    ])

    chain = prompt | llm

    print("  Sending: 'What is AVP in 10 words or less?'")
    print()

    response = chain.invoke({"input": "What is AVP in 10 words or less?"})

    print("  " + "-" * 50)
    print(f"  Response: {response.content}")
    print("  " + "-" * 50)
    print()
    print("  ✅ LangChain working with AVP credentials!")

except Exception as e:
    print(f"  ❌ Chain failed: {e}")

print()
print("=" * 60)
print("KEY TAKEAWAY")
print("=" * 60)
print()
print("Instead of:")
print('  llm = ChatAnthropic()  # Reads from ANTHROPIC_API_KEY env var')
print()
print("Use:")
print('  credentials = AVPCredentialProvider(".avp_vault.enc")')
print('  llm = ChatAnthropic(api_key=credentials.get("anthropic_api_key"))')
print()
print("Your API keys are now encrypted at rest!")
print()

credentials.close()
