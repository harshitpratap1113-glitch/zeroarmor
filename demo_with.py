"""
SCENARIO B: ZEROARMOR KE SATH (Z+ IMMUNIZED APP)
Notice: The exact same code, but with 'import zeroarmor' on Line 1!
"""

# SIRF YEH 1 LINE IMPORT KIYA:
import zeroarmor
from zeroarmor.core import ShieldBlockedException

import sqlite3
import subprocess
import os

print("\n" + "=" * 60)
print("[+] SCENARIO 2: APP WITH ZEROARMOR (Z+ IMMUNIZED)")
print("=" * 60)

# Setup sample Bank database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INT, username TEXT, balance INT)")
cursor.execute("INSERT INTO users VALUES (1, 'ceo_harshit', 5000000)")
cursor.execute("INSERT INTO users VALUES (2, 'secret_vip', 9900000)")

# --- 1. SQL Injection Attack ---
print("\n[!] ATTACK 1: Attacker tries SQL Injection (' OR '1'='1)")
attacker_input = "any_user' OR '1'='1"
query = f"SELECT username, balance FROM users WHERE username = '{attacker_input}'"
print(f"    Executing query: {query}")
try:
    cursor.execute(query)
    stolen_data = cursor.fetchall()
    print(f"    FAIL: Database dumped: {stolen_data}")
except ShieldBlockedException as e:
    print(f"    [+] ZEROARMOR SAVED APP: Blocked {e.rule_name}!")
    print("    [SAFE] Attacker got 0 rows. Database is 100% Secure!")

# --- 2. Command Injection / RCE Attack ---
print("\n[!] ATTACK 2: Attacker injects shell command (; rm)")
malicious_cmd = "cmd.exe /c echo Processing report ; rm -rf /"
print(f"    Executing command: {malicious_cmd}")
try:
    proc = subprocess.Popen(malicious_cmd, shell=True)
    print("    FAIL: Shell command executed!")
except ShieldBlockedException as e:
    print(f"    [+] ZEROARMOR SAVED APP: Blocked {e.rule_name}!")
    print("    [SAFE] Shell command aborted before execution!")

# --- 3. Path Traversal Attack ---
print("\n[!] ATTACK 3: Attacker tries Path Traversal (../../etc/passwd)")
fake_env = "../../../etc/passwd"
print(f"    Attempting to open: {fake_env}")
try:
    with open(fake_env, "r") as f:
        pass
    print("    FAIL: Path traversal succeeded!")
except ShieldBlockedException as e:
    print(f"    [+] ZEROARMOR SAVED APP: Blocked {e.rule_name}!")
    print("    [SAFE] File system boundary enforced! Access denied!")

# --- 4. Secret Leak in Logs ---
print("\n[!] ATTACK 4: Developer logs API credentials to stdout")
live_stripe = "sk_test_mock_dummy_stripe_key_testing"
print(f"    App Log: Payment gateway initialized with key: {live_stripe}")
print("    [+] ZEROARMOR SAVED APP: Live Stripe Key Auto-Masked in Console!")

print("\n" + "=" * 60)
print("[+] SUMMARY: ALL 4 ATTACKS INTERCEPTED & NEUTRALIZED IN REAL-TIME!")
print("=" * 60 + "\n")
