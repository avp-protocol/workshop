# AVP Protocol Workshop

Hands-on demos and tutorials for the Agent Vault Protocol.

## Overview

This workshop teaches you how to secure AI agent credentials using AVP. Each demo builds on the previous one, taking you from basic usage to hardware-secured deployments.

## Prerequisites

- Python 3.9+
- An API key (Anthropic, OpenAI, or similar)
- 15-30 minutes per demo

## Demos

| # | Demo | Description | Difficulty |
|---|------|-------------|------------|
| 01 | [OpenClaw Basic](demos/01-openclaw-basic/) | Replace insecure keys.json with AVP | Beginner |
| 02 | [LangChain + AVP](demos/02-langchain-avp/) | Secure LangChain credentials | Beginner |
| 03 | [CrewAI + AVP](demos/03-crewai-avp/) | Multi-agent credential management | Intermediate |
| 04 | [Hardware Security](demos/04-hardware-security/) | NexusClaw hardware key integration | Advanced |

## Quick Start

```bash
# Clone this repo
git clone https://github.com/avp-protocol/workshop.git
cd workshop

# Start with Demo 01
cd demos/01-openclaw-basic
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Follow the README in each demo folder
```

## What You'll Learn

- **Demo 01**: Migrate from plaintext credentials to encrypted AVP storage
- **Demo 02**: Integrate AVP with LangChain for secure LLM applications
- **Demo 03**: Manage credentials across multiple CrewAI agents
- **Demo 04**: Use hardware security keys for maximum protection

## The Problem We're Solving

Most AI agent frameworks store API keys insecurely:

```
# Bad: Plaintext in environment
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Bad: Plaintext in .env file
ANTHROPIC_API_KEY=sk-ant-api03-...

# Bad: Plaintext in keys.json
{"anthropic_api_key": "sk-ant-api03-..."}
```

These are trivially stolen by:
- Infostealer malware
- Compromised dependencies
- Accidental git commits
- Process memory dumps

## The AVP Solution

```python
# Good: Encrypted AVP vault
import avp

vault = avp.Vault("avp.toml")
api_key = vault.retrieve("anthropic_api_key")
# Key is encrypted at rest, never touches disk in plaintext
```

## Resources

- [AVP Specification](https://github.com/avp-protocol/spec)
- [AVP Python SDK](https://github.com/avp-protocol/avp-py)
- [AVP Website](https://avp-protocol.github.io/website)

## License

Apache 2.0
