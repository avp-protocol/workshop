#!/usr/bin/env python3
"""
Demo 03 - Step 3: Workspace Isolation

Demonstrate how AVP isolates credentials between agent workspaces.
"""

from pathlib import Path

if not Path(".avp_vault.enc").exists():
    print("❌ Vault not found. Run 01_setup_agents.py first.")
    exit(1)

print("=" * 60)
print("WORKSPACE ISOLATION DEMO")
print("=" * 60)
print()

from avp_crewai import AVPCredentialManager

manager = AVPCredentialManager(".avp_vault.enc")

print("AVP workspaces provide credential isolation between agents.")
print("Each agent can only access credentials in its own workspace.")
print()

# Show workspace contents
print("Current workspace contents:")
print("-" * 40)

workspaces = ["researcher", "writer", "analyst", "shared"]
for ws in workspaces:
    try:
        creds = manager.list_credentials(ws)
        print(f"\n  [{ws}]")
        for cred in creds:
            print(f"    • {cred}")
    except Exception as e:
        print(f"\n  [{ws}] - Error: {e}")

print()
print()

# Demonstrate isolation
print("=" * 60)
print("ISOLATION TEST")
print("=" * 60)
print()

# Add a secret credential to researcher workspace
print("1. Adding 'secret_data' to 'researcher' workspace only...")
manager.set("researcher", "secret_data", "researcher-only-secret-12345")
print("   ✅ Added to researcher workspace")
print()

# Try to access from other workspaces
print("2. Attempting to access 'secret_data' from each workspace:")
print()

for ws in ["researcher", "writer", "analyst"]:
    try:
        value = manager.get(ws, "secret_data")
        print(f"   [{ws}] ✅ Access granted: {value[:20]}...")
    except Exception as e:
        print(f"   [{ws}] ❌ Access denied (secret not in this workspace)")

print()
print("=" * 60)
print("KEY INSIGHT")
print("=" * 60)
print()
print("Each workspace is completely isolated:")
print()
print("  • Researcher can't access Writer's credentials")
print("  • Writer can't access Analyst's credentials")
print("  • No cross-workspace credential leakage")
print()
print("This is crucial for multi-agent security:")
print()
print("  1. Compromised agent can't access other agents' secrets")
print("  2. Different agents can have different permission levels")
print("  3. Audit logs show exactly which agent accessed what")
print()

# Clean up test data
print("Cleaning up test data...")
try:
    session = manager._get_session("researcher")
    manager._client.delete(session, "secret_data")
    print("✅ Test data removed")
except:
    pass

print()
manager.print_audit_log()

manager.close()
