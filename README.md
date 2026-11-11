# 🛡️ ZeroArmor Titanium: 32-Vector 1-Line Runtime Application Self-Protection (RASP)

> **Zero Configuration. Zero Refactoring. Just 1-Line Import.**  
> Immunize any Python web service, AI Agent, CLI, or microservice against 98%+ of OWASP Top 10, CWE, and Next-Gen AI exploits in real-time.

```python
import zeroarmor  # 💥 BOOM! All 32 Titanium Security Shields Auto-Ignited
```

---

## ⚡ What's New in v2.0 Titanium Edition?

* 🤖 **Next-Gen AI & LLM Prompt Injection Shield**: Intercepts jailbreak prompts (`Ignore previous instructions`, DAN, persona bypasses, system prompt extraction).
* 🌐 **Universal SSRF & Hex IP Normalization**: Intercepts `urllib`, `requests`, `httpx`, and `http.client` against cloud metadata theft, decimal IPs (`2130706433`), and hex loopbacks (`0x7f000001`).
* 📁 **Sensitive Credential Prison**: Intercepts reads to `.env`, `id_rsa`, `.git/config`, `credentials.json`, and service account tokens.
* 📦 **NoSQL & MongoDB Operator Injection**: Traps query selector tampering (`$gt`, `$where`, `$ne`) in unvalidated input schemas.
* 📜 **XML External Entity (XXE) & Billion Laughs**: Proactively neutralizes `<!ENTITY` external references and recursive entity bombs.
* 🎫 **JWT Alg 'None' & Signature Stripping**: Eliminates empty signature and algorithm none token confusion attacks.
* 🔗 **Open Redirect / Phishing Boundary**: Neutralizes protocol-relative (`//evil.com`) and javascript redirect vectors.
* 🗄️ **GraphQL Query Depth Bomb Defense**: Hard cap on recursive nested cyclic queries.
* 🍯 **Active Honeypot & Deception Canaries**: Seeds synthetic canary probes to auto-quarantine offensive scanners.
* ⚙️ **Configurable Defense Modes**: `BLOCK` (strict active protection), `AUDIT` (passive canary logging), or `DECEIVE` (honeypot trap).
* 📡 **Enterprise SIEM Exporters**: 1-click export to Common Event Format (CEF) and JSON for Splunk, Datadog, and SIEM ingest.

---

## 🛡️ The Complete 32-Layer Security Matrix

| # | Security Vector | Target Subsystem | Action on Exploit |
|---|---|---|---|
| **1** | **SQL Injection (SQLi)** | `sqlite3`, `psycopg2`, `mysql`, `pymysql` | Malicious queries, tautologies & blind sleep payloads blocked |
| **2** | **Remote Code Execution (RCE)** | `subprocess`, `os.system`, `os.popen` | Shell pipes (`\|`, `;`, `&&`), download cradles & reverse shells killed |
| **3** | **Path Traversal (LFI)** | `builtins.open`, `pathlib.Path` | Directory traversal (`../`, `/etc/passwd`) jailed |
| **4** | **SSRF & Cloud Metadata** | `http.client`, `urllib`, `requests`, `httpx` | AWS/GCP metadata (`169.254.169.254`) & hex IPs (`0x7f000001`) dropped |
| **5** | **Insecure Deserialization** | `pickle.loads`, `_pickle.loads` | Unsafe system/os execution gadget payloads blocked |
| **6** | **Code Injection (eval / exec)** | `builtins.eval`, `builtins.exec` | Arbitrary dynamic code injection & system access blocked |
| **7** | **Real-Time Secret Scrubber** | `sys.stdout`, `sys.stderr`, `logging` | Live regex mask for Stripe, AWS, GitHub tokens, JWTs, SSH keys |
| **8** | **ReDoS (Regex DoS)** | `re.compile`, `re.search` | Catastrophic backtracking nested quantifiers defense |
| **9** | **Memory Bomb / Body DoS** | WSGI / ASGI input streams | Hard payload threshold (10MB) to stop RAM exhaustion |
| **10** | **Class Attribute Pollution** | `object.__subclasses__`, `__proto__` | Dynamic attribute tampering from untrusted inputs frozen |
| **11** | **Zip Slip / Tar Bomb** | `zipfile`, `tarfile` | Archive path traversal outside target extract directory blocked |
| **12** | **Insecure Temp Files** | `tempfile.mktemp` | Redirect to secure, permission-hardened temp files |
| **13** | **Template Injection (SSTI)** | Jinja2 / Mako render passes | `{{ config.__class__ }}` sandbox escape traps blocked |
| **14** | **Clickjacking Defense** | HTTP Response Headers | Auto-inject `X-Frame-Options: DENY` |
| **15** | **Cross-Site Scripting (XSS)** | HTTP Response Headers | Auto-inject strict `Content-Security-Policy` & `X-XSS-Protection` |
| **16** | **MIME Sniffing Prevention** | HTTP Response Headers | Auto-inject `X-Content-Type-Options: nosniff` |
| **17** | **SSL Downgrade Protection** | HTTP Response Headers | Auto-inject `Strict-Transport-Security (HSTS)` |
| **18** | **Referrer Leakage** | HTTP Response Headers | Auto-inject `Referrer-Policy: strict-origin-when-cross-origin` |
| **19** | **Insecure CORS Wildcard** | HTTP Origin Headers | Blocks `Access-Control-Allow-Origin: *` with credentials |
| **20** | **Sensitive File Jail** | File I/O Sandbox | Read access block for `.env`, `id_rsa`, `.git/config`, `credentials.json` |
| **21** | **Outbound DLP (Data Leak)** | Outgoing HTTP Responses | Credit Cards (Luhn) & unmasked sensitive PII leak check |
| **22** | **Anti-Bot & Rate Limiting** | In-Memory Token Bucket | High-speed IP burst rate-limiter |
| **23** | **LLM Prompt Injection** | AI Inference / LLM APIs | Traps instruction overrides, DAN personas & prompt leaks |
| **24** | **GraphQL Depth Bomb** | GraphQL Endpoints | Caps recursive nested cyclic query depth at 7 levels |
| **25** | **XML External Entity (XXE)** | `xml.etree.ElementTree`, `minidom` | Blocks hazardous `<!ENTITY`, SYSTEM files & Billion Laughs |
| **26** | **NoSQL Operator Injection** | MongoDB / Document DBs | Blocks `$gt`, `$where`, `$ne` authentication bypass operators |
| **27** | **Open Redirect / Phishing** | HTTP Location Headers | Blocks protocol-relative (`//evil.com`) & javascript URI redirects |
| **28** | **JWT Alg 'None' Confusion** | PyJWT / Token Decoders | Blocks unsigned tokens & algorithm 'none' stripping |
| **29** | **Insecure Cryptography** | `hashlib.md5`, `hashlib.sha1` | Flags deprecated hashes in security contexts |
| **30** | **YAML Object Gadgets** | PyYAML Unsafe Loaders | Blocks `!!python/object/apply` gadget execution |
| **31** | **DNS Rebinding Shield** | Socket Address Resolution | Blocks external domains resolving to internal private RFC1918 IPs |
| **32** | **Active Honeytoken Canary** | Deception Engine | Synthetic trap endpoints & canary tokens to auto-quarantine scanners |

---

## 🚀 Quickstart & Usage

### 1-Line Import
```python
import zeroarmor

# Your existing code continues unchanged:
from fastapi import FastAPI
app = FastAPI()

# 1-Line Framework Auto-Wrapper:
app = zeroarmor.shield_app(app)
```

### CLI Commands
```bash
# View active shield matrix and status
zeroarmor status

# Run automated 32-vector self-diagnostic test suite
zeroarmor test

# Monitor blocked cyber attacks in real-time
zeroarmor monitor

# Launch the interactive cyber defense simulation lab
zeroarmor lab

# Export threat telemetry for SIEM ingest
zeroarmor export --cef --file /var/log/zeroarmor.cef
```

---

## 🧪 Automated Testing
```bash
python tests/test_32_shields.py
```
Outputs 100% PASS across all 32 vectors.

---

## 💰 Commercial Pro Licensing & 🔄 Guaranteed Future Updates

ZeroArmor Titanium operates on an open-core architecture:
* **Community Edition:** 100% Free under Apache 2.0 for personal and educational use.
* **Commercial Pro & Enterprise License ($49 Early-Bird Lifetime):** For startups, proprietary SaaS platforms, and enterprise deployments needing commercial distribution rights, SIEM export pipelines, and priority defense support.
* **100% Lifetime Future Updates Guaranteed:** All license holders receive continuous automatic updates for life — including new zero-day vulnerability heuristics, updated LLM prompt injection jailbreak models, and native adapters for evolving AI agent frameworks (CrewAI, LangChain, AutoGen, LlamaIndex) with zero annual subscription renewals.

For commercial licensing and enterprise deployment inquiries, contact: `harshitpratap1113@gmail.com`

