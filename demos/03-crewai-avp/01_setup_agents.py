#!/usr/bin/env python3
"""
Demo 03 - Step 1: Set up credentials for multi-agent system

Creates workspaces and credentials for different agents/roles.
"""

import getpass
from pathlib import Path

from avp import AVPClient
from avp.backends import FileBackend

print("=" * 60)
print("CREWAI MULTI-AGENT CREDENTIAL SETUP")
print("=" * 60)
print()

vault_path = Path(".avp_vault.enc")

# Get or create vault
if vault_path.exists():
    print(f"Using existing vault: {vault_path}")
    password = getpass.getpass("Enter vault password: ")
else:
    print("Creating new vault...")
    password = getpass.getpass("Choose vault password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        print("Passwords don't match!")
        exit(1)

print()

# Connect
backend = FileBackend(str(vault_path), password)
client = AVPClient(backend)

# Define agent workspaces
workspaces = {
    "researcher": "Research agent - web search, data gathering",
    "writer": "Writer agent - content generation",
    "analyst": "Analyst agent - data analysis, insights",
    "shared": "Shared credentials for all agents"
}

print("This demo sets up credentials for multiple agent workspaces:")
print()
for ws, desc in workspaces.items():
    print(f"  • {ws}: {desc}")
print()

# Get API key (will be stored in shared workspace)
print("Enter your API credentials:")
print("(These will be stored in each workspace for demonstration)")
print()

api_key = getpass.getpass("API Key (Anthropic or OpenAI): ")
if not api_key.strip():
    print("No API key entered. Exiting.")
    exit(1)

# Detect key type
if api_key.startswith("sk-ant"):
    key_name = "anthropic_api_key"
    key_type = "Anthropic"
else:
    key_name = "openai_api_key"
    key_type = "OpenAI"

print()
print(f"Detected: {key_type} API key")
print()

# Store credentials in each workspace
print("Setting up workspaces...")
print()

for workspace in workspaces:
    session = client.authenticate(workspace=workspace)

    # Store the API key
    client.store(session.session_id, key_name, api_key.encode())

    # Add workspace-specific metadata
    client.store(
        session.session_id,
        "workspace_info",
        f"Workspace: {workspace}\nCreated for CrewAI demo".encode()
    )

    print(f"  ✅ {workspace}: {key_name} stored")

print()
print("=" * 60)
print("SETUP COMPLETE")
print("=" * 60)
print()
print("Workspaces created:")
for ws in workspaces:
    print(f"  • {ws}")
print()
print("Each workspace has isolated credentials.")
print("Agents can only access their own workspace.")
print()
print("Next: Run 02_basic_crew.py to see multi-agent credentials in action")
print()

client.close()
