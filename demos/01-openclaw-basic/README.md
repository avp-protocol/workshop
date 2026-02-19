# Demo 01: OpenClaw + AVP Basic Integration

Replace OpenClaw's insecure `keys.json` with AVP encrypted storage.

## Time Required
15-20 minutes

## What You'll Learn
- Set up AVP with the Python SDK
- Store API credentials securely
- Integrate AVP with OpenClaw agents
- Migrate existing credentials

## Prerequisites
- Python 3.9+
- An Anthropic or OpenAI API key

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 1: The Problem (Insecure Approach)

First, let's see how credentials are typically stored (DON'T DO THIS):

```python
# insecure_example.py - THIS IS BAD!
import os

# Bad: Environment variable (visible in process list)
api_key = os.environ.get("ANTHROPIC_API_KEY")

# Bad: Hardcoded (committed to git)
api_key = "sk-ant-api03-xxxxx"

# Bad: Plaintext file (stolen by malware)
with open("keys.json") as f:
    api_key = json.load(f)["anthropic_api_key"]
```

Run the insecure example to see the risks:
```bash
python 01_insecure_example.py
```

## Step 2: The AVP Solution

Now let's use AVP to store credentials securely:

```bash
python 02_setup_vault.py
```

This script will:
1. Create an AVP vault with encrypted storage
2. Prompt you for your API key
3. Store it securely (encrypted at rest)

## Step 3: Using AVP with OpenClaw

Run the secure OpenClaw agent:

```bash
python 03_openclaw_agent.py
```

This demonstrates:
- Retrieving credentials from AVP
- Using them with an OpenClaw agent
- Credentials never touch disk in plaintext

## Step 4: Migration (Optional)

If you have existing credentials in `keys.json`:

```bash
python 04_migrate_credentials.py
```

This will:
1. Read your existing `keys.json`
2. Import all credentials into AVP
3. Securely delete the plaintext file

## File Structure

```
01-openclaw-basic/
├── README.md              # This file
├── requirements.txt       # Dependencies
├── 01_insecure_example.py # What NOT to do
├── 02_setup_vault.py      # Set up AVP vault
├── 03_openclaw_agent.py   # Secure OpenClaw usage
├── 04_migrate_credentials.py  # Migration helper
└── avp.toml              # AVP configuration (created by setup)
```

## Security Comparison

| Approach | Infostealer | Memory Dump | Git Leak |
|----------|:-----------:|:-----------:|:--------:|
| Environment vars | ❌ Exposed | ❌ Exposed | ✅ Safe |
| .env file | ❌ Exposed | ❌ Exposed | ❌ Risk |
| keys.json | ❌ Exposed | ❌ Exposed | ❌ Risk |
| **AVP (file)** | ✅ Encrypted | ❌ Exposed | ✅ Safe |
| **AVP (keychain)** | ✅ Encrypted | ✅ Protected | ✅ Safe |

## Next Steps

- [Demo 02: LangChain + AVP](../02-langchain-avp/) - Secure LangChain applications
- [Demo 04: Hardware Security](../04-hardware-security/) - Maximum protection with NexusClaw

## Troubleshooting

**Q: I get "ModuleNotFoundError: No module named 'avp'"**
```bash
pip install avp-sdk
```

**Q: How do I reset the vault?**
```bash
rm -rf ~/.avp/  # Remove vault data
python 02_setup_vault.py  # Re-run setup
```

**Q: Can I use a different backend?**
Yes! Edit `avp.toml` to use `keychain` or `hardware` backend.
