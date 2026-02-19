#!/usr/bin/env python3
"""
Demo 04 - Step 1: Understanding Security Levels

Compare different credential storage approaches and their security properties.
"""

print("=" * 70)
print("CREDENTIAL SECURITY LEVELS")
print("=" * 70)
print()

# Security level visualization
security_diagram = """
┌─────────────────────────────────────────────────────────────────────┐
│                      SECURITY HIERARCHY                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ████████████████████  LEVEL 4: HARDWARE (NexusClaw)               │
│  ████████████████████  • Credentials NEVER leave the device        │
│  ████████████████████  • Tamper-resistant secure element           │
│  ████████████████████  • Physical touch required for each use      │
│                        • Self-destructs after failed PIN attempts  │
│                                                                     │
│  ████████████████░░░░  LEVEL 3: OS KEYCHAIN                        │
│  ████████████████░░░░  • Protected by OS security model            │
│  ████████████████░░░░  • Encrypted by user login password          │
│                        • Vulnerable to privileged malware          │
│                        • No physical presence requirement          │
│                                                                     │
│  ████████████░░░░░░░░  LEVEL 2: ENCRYPTED FILE (AVP File Backend)  │
│  ████████████░░░░░░░░  • Encrypted at rest with AES-256            │
│                        • Master password in memory during use      │
│                        • Vulnerable to memory dumps                │
│                        • Protects against basic file theft         │
│                                                                     │
│  ████░░░░░░░░░░░░░░░░  LEVEL 1: PLAINTEXT                          │
│  ████░░░░░░░░░░░░░░░░  • .env files, keys.json, env vars           │
│                        • Zero protection                           │
│                        • Trivially stolen by any malware           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
"""

print(security_diagram)
print()

# Attack vector comparison
print("=" * 70)
print("ATTACK VECTOR COMPARISON")
print("=" * 70)
print()

attacks = [
    ("Infostealer Malware", "Scans disk for credential files",
     ["❌ Exposed", "✅ Encrypted", "✅ Protected", "✅ Protected"]),

    ("Memory Dump", "Extracts secrets from RAM",
     ["❌ Exposed", "❌ Exposed", "❌ Exposed", "✅ Protected"]),

    ("Process Injection", "Injects code to steal credentials",
     ["❌ Exposed", "❌ Exposed", "❌ Exposed", "✅ Protected"]),

    ("Accidental Git Commit", "Credentials pushed to repo",
     ["❌ Exposed", "✅ Safe", "✅ Safe", "✅ Safe"]),

    ("Shoulder Surfing", "Attacker views screen",
     ["❌ Exposed", "✅ Masked", "✅ Masked", "✅ Masked"]),

    ("Physical Device Theft", "Laptop stolen",
     ["❌ Exposed", "⚠️ Password", "⚠️ Login", "✅ PIN + Touch"]),

    ("Side-Channel Attack", "CPU behavior analysis",
     ["N/A", "❌ Vulnerable", "❌ Vulnerable", "✅ Protected"]),
]

print(f"{'Attack Vector':<25} {'Plaintext':<12} {'Encrypted':<12} {'Keychain':<12} {'Hardware':<12}")
print("-" * 70)

for attack, desc, results in attacks:
    print(f"{attack:<25} {results[0]:<12} {results[1]:<12} {results[2]:<12} {results[3]:<12}")

print()
print()

# Recommendations
print("=" * 70)
print("RECOMMENDATIONS")
print("=" * 70)
print()

recommendations = """
USE PLAINTEXT (Level 1): NEVER
  Don't use .env files, environment variables, or keys.json for
  production credentials.

USE ENCRYPTED FILE (Level 2): Development & Testing
  Good for local development where convenience matters more than
  maximum security. Protects against basic file theft.

USE OS KEYCHAIN (Level 3): Production (Standard)
  Good balance of security and convenience for most production
  workloads. Credentials protected by OS security model.

USE HARDWARE (Level 4): Production (High-Security)
  Use for high-value credentials:
  • API keys with high billing limits
  • Access to sensitive data (PII, financial)
  • Compliance-sensitive environments
  • High-value targets (admin, crypto)
"""

print(recommendations)
print()

# Real-world cost of compromise
print("=" * 70)
print("REAL-WORLD COST OF COMPROMISE")
print("=" * 70)
print()

costs = """
SCENARIO: Anthropic API key stolen by infostealer malware

IF STORED IN PLAINTEXT (.env file):
  • Attacker finds key instantly
  • Makes unlimited API calls
  • Your bill: $10,000+ in hours
  • Your data: Potentially exfiltrated through your agents

IF STORED IN AVP (Encrypted File):
  • Attacker gets encrypted blob
  • Can't decrypt without master password
  • Must also capture password from memory
  • Attack complexity: Much higher

IF STORED IN HARDWARE (NexusClaw):
  • Attacker gets nothing usable
  • Credential never leaves device
  • Would need physical device + PIN
  • Device self-destructs after failed attempts
"""

print(costs)
print()
print("Next: Run 02_setup_nexusclaw.py to set up hardware security")
print()
