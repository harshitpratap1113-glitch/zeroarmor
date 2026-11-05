# 🛡️ ZeroArmor: 22-Vector 1-Line Runtime Application Self-Protection (RASP)

> **Zero Configuration. Zero Refactoring. Just 1-Line Import.**  
> Immunize any Python web service, CLI, or backend against 90%+ of OWASP Top 10 exploits in real-time.

```python
import zeroarmor  # 💥 BOOM! All 22 Z+ Security Shields Auto-Ignited
```

---

## ⚡ Why ZeroArmor?

Traditional security forces developers to configure complex WAFs, write 500 lines of manual input validation, or pay $1,000s/month to enterprise vendors.

**ZeroArmor flips the paradigm:**
* **Instant:** Auto-executes upon import in under 2 milliseconds.
* **Non-Invasive:** Normal database queries, valid shell calls, and benign file opens run at 100% native speed.
* **Zero Refactoring:** You don't have to change a single line of your business code.

---

## 🛡️ The 22-Layer Security Matrix

| # | Security Vector | Target Subsystem | Action on Exploit |
|---|---|---|---|
| **1** | **SQL Injection (SQLi)** | `sqlite3`, `psycopg2`, `mysql`, `pymysql` | Malicious unparameterized queries & tautologies blocked |
| **2** | **Remote Code Execution (RCE)** | `subprocess`, `os.system`, `os.popen` | Chained shell pipes (`\|`, `;`, `&&`, `$()`) killed |
| **3** | **Path Traversal (LFI)** | `builtins.open`, `pathlib.Path` | Directory traversal (`../`, `/etc/passwd`, `.env`) jailed |
| **4** | **SSRF & Cloud Metadata** | `urllib.request`, `requests`, `http.client` | `169.254.169.254`, `127.0.0.1`, private IP ranges dropped |
| **5** | **Insecure Deserialization** | `pickle.loads`, `_pickle.loads`, `yaml.load` | Unsafe gadget payloads blocked; `safe_load` enforced |
| **6** | **Code Injection (eval / exec)** | `builtins.eval`, `builtins.exec` | Arbitrary dynamic code injection & system access blocked |
| **7** | **Real-Time Secret Scrubber** | `sys.stdout`, `sys.stderr`, `logging` | Live regex mask for Stripe, AWS, GitHub tokens, JWTs |
| **8** | **ReDoS (Regex DoS)** | `re.compile`, `re.search` | Catastrophic backtracking nested quantifiers defense |
| **9** | **Memory Bomb / Body DoS** | WSGI / ASGI input streams | Hard memory cap (10MB) to stop RAM exhaustion |
| **10** | **Class Attribute Pollution** | `object.__subclasses__`, `__dict__` | Dynamic attribute tampering from untrusted inputs frozen |
| **11** | **Zip Slip / Tar Bomb** | `zipfile`, `tarfile` | Archive path traversal outside target extract directory blocked |
| **12** | **Insecure Temp Files** | `tempfile.mktemp` | Redirect to secure, permission-hardened temp files |
| **13** | **Template Injection (SSTI)** | Jinja2 / Mako render passes | `{{ config.__class__ }}` payload traps blocked |
| **14** | **Clickjacking Defense** | HTTP Response Headers | Auto-inject `X-Frame-Options: DENY` |
| **15** | **Cross-Site Scripting (XSS)** | HTTP Response Headers | Auto-inject strict `Content-Security-Policy` & `X-XSS-Protection` |
| **16** | **MIME Sniffing Prevention** | HTTP Response Headers | Auto-inject `X-Content-Type-Options: nosniff` |
| **17** | **SSL Downgrade Protection** | HTTP Response Headers | Auto-inject `Strict-Transport-Security (HSTS)` |
| **18** | **Referrer Leakage** | HTTP Response Headers | Auto-inject `Referrer-Policy: strict-origin-when-cross-origin` |
| **19** | **Insecure CORS Wildcard** | HTTP Origin Headers | Blocks `Access-Control-Allow-Origin: *` with credentials |
| **20** | **Sensitive File Jail** | File I/O Sandbox | Read access block for `.git/`, `.env`, `id_rsa`, `config.json` |
| **21** | **Outbound DLP (Data Leak)** | Outgoing HTTP Responses | Credit Cards (Luhn) & Aadhaar/SSN unmasked leak check |
| **22** | **Anti-Bot & Rate Limiting** | In-Memory Token Bucket | High-speed IP burst rate-limiter |

---

## 🚀 Installation & Quickstart

### Option A: Direct Pip Install (1-Line — Works Everywhere)
```bash
pip install https://github.com/harshitpratap1113-glitch/zeroarmor/releases/download/v1.0.0/zeroarmor-1.0.0-py3-none-any.whl
```

### Option B: Via Git
```bash
pip install git+https://github.com/harshitpratap1113-glitch/zeroarmor.git
```

### Option C: Via PEP 503 PyPI Index
```bash
pip install zeroarmor --extra-index-url https://harshitpratap1113-glitch.github.io/zeroarmor/simple/
```
*(Tip: Run `pip config set global.extra-index-url https://harshitpratap1113-glitch.github.io/zeroarmor/simple/` once, and then you can simply run `pip install zeroarmor` forever!)*

### Option D: Via Conda
```bash
conda install -c https://harshitpratap1113-glitch.github.io/zeroarmor/conda zeroarmor
```
*(Tip: Run `conda config --add channels https://harshitpratap1113-glitch.github.io/zeroarmor/conda` once, and then you can simply run `conda install zeroarmor` forever!)*

### Option E: 1-Click Automated Terminal Installers
* **Windows (PowerShell):**
  ```powershell
  irm https://raw.githubusercontent.com/harshitpratap1113-glitch/zeroarmor/master/install.ps1 | iex
  ```
* **Linux / macOS (Bash):**
  ```bash
  curl -sSL https://raw.githubusercontent.com/harshitpratap1113-glitch/zeroarmor/master/install.sh | bash
  ```

---

## ⚡ Usage in Your Code
```python
import zeroarmor

# That's it! Your entire backend is now protected.
```

---

## 🧪 Live Demo
Run the included real-world vulnerability showcase:
```bash
python demo_vulnerable_app.py
```

Run the full automated test suite:
```bash
python tests/test_20_shields.py
```

---

## 🌐 FastAPI / Flask Middleware (Optional)
If you also want automated HTTP Header injection and Outbound Data Loss Prevention on web responses:
```python
from fastapi import FastAPI
from zeroarmor.middleware import ZeroArmorMiddleware

app = FastAPI()
app.add_middleware(ZeroArmorMiddleware)
```

---

## 📄 License
Apache-2.0 License. Free Community Edition for all developers and startups.
Built by **ZeroArmor Cyber Defense Labs**.
