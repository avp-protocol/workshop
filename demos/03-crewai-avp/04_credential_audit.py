#!/usr/bin/env python3
"""
Demo 03 - Step 4: Credential Auditing

Shows how AVP tracks credential access for compliance and debugging.
"""

from pathlib import Path
from datetime import datetime

if not Path(".avp_vault.enc").exists():
    print("❌ Vault not found. Run 01_setup_agents.py first.")
    exit(1)

print("=" * 60)
print("CREDENTIAL ACCESS AUDITING")
print("=" * 60)
print()

from avp_crewai import AVPCredentialManager

manager = AVPCredentialManager(".avp_vault.enc")

print("AVP tracks all credential access for auditing and debugging.")
print()

# Simulate various credential operations
print("Simulating agent credential access...")
print("-" * 40)
print()

# Researcher accesses credentials
print("1. Researcher agent starting up...")
creds = manager.list_credentials("researcher")
api_key = manager.get("researcher", creds[0])
print(f"   Retrieved: {creds[0]}")

# Writer accesses credentials
print("2. Writer agent starting up...")
creds = manager.list_credentials("writer")
api_key = manager.get("writer", creds[0])
print(f"   Retrieved: {creds[0]}")

# Analyst accesses credentials
print("3. Analyst agent starting up...")
creds = manager.list_credentials("analyst")
api_key = manager.get("analyst", creds[0])
print(f"   Retrieved: {creds[0]}")

# Researcher rotates a credential
print("4. Researcher rotating credentials...")
manager.set("researcher", "temp_token", "temp-value-123")
manager.rotate("researcher", "temp_token", "rotated-value-456")
print("   Rotated: temp_token")

print()

# Show full audit log
print("=" * 60)
print("FULL AUDIT LOG")
print("=" * 60)
manager.print_audit_log()

# Analyze the audit log
print()
print("=" * 60)
print("AUDIT ANALYSIS")
print("=" * 60)
print()

audit_log = manager.get_audit_log()

# Count by workspace
workspace_counts = {}
for entry in audit_log:
    ws = entry["workspace"]
    workspace_counts[ws] = workspace_counts.get(ws, 0) + 1

print("Access by workspace:")
for ws, count in sorted(workspace_counts.items()):
    print(f"  • {ws}: {count} operations")

print()

# Count by action type
action_counts = {}
for entry in audit_log:
    action = entry["action"]
    action_counts[action] = action_counts.get(action, 0) + 1

print("Access by operation type:")
for action, count in sorted(action_counts.items()):
    print(f"  • {action}: {count}")

print()

# Show credentials accessed
credentials_accessed = set()
for entry in audit_log:
    if entry.get("credential"):
        credentials_accessed.add(entry["credential"])

print("Credentials accessed:")
for cred in sorted(credentials_accessed):
    print(f"  • {cred}")

print()
print("=" * 60)
print("WHY AUDITING MATTERS")
print("=" * 60)
print()
print("1. SECURITY INCIDENT RESPONSE")
print("   If a key is compromised, you know exactly:")
print("   - Which agents accessed it")
print("   - When it was accessed")
print("   - What operations were performed")
print()
print("2. COMPLIANCE")
print("   Demonstrate credential handling for:")
print("   - SOC 2 audits")
print("   - Security reviews")
print("   - Internal compliance")
print()
print("3. DEBUGGING")
print("   Understand agent behavior:")
print("   - Which credentials each agent needs")
print("   - Access patterns over time")
print("   - Unexpected access attempts")
print()

# Clean up
try:
    session = manager._get_session("researcher")
    manager._client.delete(session, "temp_token")
except:
    pass

manager.close()
print("Session complete.")
