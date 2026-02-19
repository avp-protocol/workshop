# Demo 02: LangChain + AVP Integration

Secure your LangChain applications with AVP credential management.

## Time Required
15-20 minutes

## What You'll Learn
- Integrate AVP with LangChain
- Create a custom credential provider
- Build a secure RAG application
- Handle multiple API keys safely

## Prerequisites
- Completed Demo 01 (or have AVP SDK installed)
- Python 3.9+
- Anthropic or OpenAI API key

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## The Problem

LangChain applications typically load credentials like this:

```python
# Insecure: from environment
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic()  # Reads ANTHROPIC_API_KEY from env

# Insecure: hardcoded
llm = ChatAnthropic(api_key="sk-ant-...")
```

Both approaches leave credentials exposed to theft.

## The Solution

```python
# Secure: from AVP vault
from avp_langchain import AVPCredentialProvider

credentials = AVPCredentialProvider("avp.toml")
llm = ChatAnthropic(api_key=credentials.get("anthropic_api_key"))
```

## Demo Steps

### Step 1: Set up credentials
```bash
python 01_setup_credentials.py
```

### Step 2: Run basic LangChain example
```bash
python 02_basic_chain.py
```

### Step 3: Build a secure RAG application
```bash
python 03_secure_rag.py
```

### Step 4: Multi-provider example
```bash
python 04_multi_provider.py
```

## File Structure

```
02-langchain-avp/
├── README.md
├── requirements.txt
├── 01_setup_credentials.py
├── 02_basic_chain.py
├── 03_secure_rag.py
├── 04_multi_provider.py
└── avp_langchain.py          # AVP-LangChain integration
```

## Security Benefits

| Feature | Without AVP | With AVP |
|---------|-------------|----------|
| Credential storage | Plaintext env | Encrypted vault |
| Multiple API keys | Multiple env vars | Single secure store |
| Key rotation | Manual update | Programmatic rotation |
| Audit trail | None | Full logging |

## Next Steps

- [Demo 03: CrewAI + AVP](../03-crewai-avp/) - Multi-agent credential management
- [Demo 04: Hardware Security](../04-hardware-security/) - Maximum protection
