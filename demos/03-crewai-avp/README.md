# Demo 03: CrewAI + AVP Multi-Agent Credential Management

Manage credentials across multiple AI agents in CrewAI applications.

## Time Required
20-25 minutes

## What You'll Learn
- Integrate AVP with CrewAI
- Manage credentials for multi-agent systems
- Implement workspace isolation per agent
- Handle credential sharing between agents

## Prerequisites
- Completed Demo 01 or 02
- Python 3.9+
- API keys for your preferred LLM provider

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## The Challenge

Multi-agent systems have unique credential requirements:

```python
# Problem: All agents share the same env var
researcher = Agent(role="Researcher")  # Uses OPENAI_API_KEY
writer = Agent(role="Writer")          # Uses same OPENAI_API_KEY
analyst = Agent(role="Analyst")        # Uses same OPENAI_API_KEY

# What if different agents need different API keys?
# What if you want to track which agent uses which credentials?
# What if agents need isolated credential namespaces?
```

## The Solution

```python
from avp_crewai import AVPCredentialManager

# Create credential manager with workspace isolation
cred_manager = AVPCredentialManager("avp.toml")

# Each agent can have its own workspace
researcher = Agent(
    role="Researcher",
    llm=cred_manager.get_llm("researcher-workspace")
)

writer = Agent(
    role="Writer",
    llm=cred_manager.get_llm("writer-workspace")
)
```

## Demo Steps

### Step 1: Set up multi-agent credentials
```bash
python 01_setup_agents.py
```

### Step 2: Run a basic crew with AVP
```bash
python 02_basic_crew.py
```

### Step 3: Workspace isolation demo
```bash
python 03_workspace_isolation.py
```

### Step 4: Credential auditing
```bash
python 04_credential_audit.py
```

## Security Benefits

| Feature | Traditional | With AVP |
|---------|-------------|----------|
| Credential storage | Shared env vars | Per-agent encrypted |
| Isolation | None | Workspace separation |
| Audit trail | Manual logging | Built-in tracking |
| Rotation | Restart required | Hot rotation |
| Access control | All or nothing | Fine-grained |

## Next Steps

- [Demo 04: Hardware Security](../04-hardware-security/) - Maximum protection with NexusClaw
