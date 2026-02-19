# Demo 04: Hardware Security with NexusClaw

Maximum credential protection using hardware security keys.

## Time Required
25-30 minutes

## What You'll Learn
- Why hardware security provides the strongest protection
- Set up NexusClaw USB security key
- Store credentials in tamper-resistant hardware
- Handle hardware key workflows

## Prerequisites
- Completed Demos 01-03 (understanding of AVP basics)
- NexusClaw USB security key (or simulation mode for learning)
- Python 3.9+

## The Security Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LEVELS                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Level 4: HARDWARE (NexusClaw)           ████████████ MAX  │
│  - Credentials never leave the device                       │
│  - Tamper-resistant secure element                          │
│  - Physical presence required                               │
│                                                             │
│  Level 3: OS KEYCHAIN                    ████████░░░░      │
│  - Protected by OS security                                 │
│  - Encrypted by user password                               │
│  - Vulnerable to privileged malware                         │
│                                                             │
│  Level 2: ENCRYPTED FILE                 █████░░░░░░░      │
│  - Encrypted at rest                                        │
│  - Password in memory during use                            │
│  - Vulnerable to memory dumps                               │
│                                                             │
│  Level 1: PLAINTEXT                      █░░░░░░░░░░░ MIN  │
│  - No protection                                            │
│  - Stolen by any malware                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Why Hardware Security?

Even with encrypted file storage, credentials must be decrypted in memory to use them. A sophisticated attacker can:

1. **Memory dump** - Extract decrypted credentials from RAM
2. **Process injection** - Inject code to steal credentials
3. **Side-channel attacks** - Observe CPU behavior during decryption

**Hardware security keys solve this** by performing cryptographic operations inside the device. The credential never leaves the secure element.

## NexusClaw Features

- **TROPIC01 Secure Element** - Military-grade tamper resistance
- **USB-C Connection** - Works with any computer
- **Physical Confirmation** - Touch required for operations
- **Self-Destruct** - Wipes on tamper detection

## Demo Steps

### Step 1: Understanding hardware security
```bash
python 01_security_levels.py
```

### Step 2: Set up NexusClaw (or simulation)
```bash
python 02_setup_nexusclaw.py
```

### Step 3: Store credentials in hardware
```bash
python 03_hardware_storage.py
```

### Step 4: Production workflow
```bash
python 04_production_workflow.py
```

## File Structure

```
04-hardware-security/
├── README.md
├── requirements.txt
├── 01_security_levels.py      # Security comparison
├── 02_setup_nexusclaw.py      # Device setup
├── 03_hardware_storage.py     # Store in hardware
├── 04_production_workflow.py  # Production patterns
└── avp_hardware.py            # Hardware backend wrapper
```

## Security Comparison

| Attack Vector | File | Keychain | Hardware |
|---------------|:----:|:--------:|:--------:|
| Malware file theft | ❌ | ✅ | ✅ |
| Memory dump | ❌ | ❌ | ✅ |
| Process injection | ❌ | ❌ | ✅ |
| Physical theft | ❌ | ❌ | ✅* |
| Side-channel | ❌ | ❌ | ✅ |

*Hardware requires PIN, self-destructs after failed attempts

## When to Use Hardware Security

**Recommended for:**
- Production API keys with high billing limits
- Keys with access to sensitive data
- Compliance-sensitive environments (healthcare, finance)
- High-value targets (crypto wallets, admin credentials)

**May be overkill for:**
- Development/testing credentials
- Low-privilege API keys
- Credentials with low blast radius

## Get NexusClaw

- [NexusClaw Product Page](https://avp-protocol.github.io/website)
- [Hardware Documentation](https://github.com/avp-protocol/nexusclaw)
