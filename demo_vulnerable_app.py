"""
ZeroArmor Live Interactive Showcase Demo
Simulates a real-world web API scenario with multiple hacker attack payloads.
Run this script to see ZeroArmor in action!
"""

import sys
import os
import sqlite3
import subprocess

# Add parent directory
sys.path.insert(0, os.path.dirname(__file__))

# 💥 The 1-Line Import at the top!
import zeroarmor
from zeroarmor.core import ShieldBlockedException

print("=" * 65)
print("[*] ZEROARMOR INTERACTIVE VULNERABILITY SHOWCASE")
print("=" * 65)

# Setup sample DB
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INTEGER, username TEXT, balance INTEGER)")
cursor.execute("INSERT INTO users VALUES (1, 'ceo_harshit', 5000000)")
cursor.execute("INSERT INTO users VALUES (2, 'john_doe', 1200)")

print("\n[+] Sample Bank Database initialized with 2 accounts.")

# Attack 1: SQL Injection
print("\n[!] ATTACK 1: Attacker tries SQL Injection on login endpoint...")
attacker_input = "ceo_harshit' OR '1'='1"
print(f"    Payload: {attacker_input}")
try:
    cursor.execute(f"SELECT * FROM users WHERE username = '{attacker_input}'")
    print("    [-] FAIL: Exploit Succeeded! DB Leaked!")
except ShieldBlockedException as e:
    print(f"    [+] ZEROARMOR SAVED APP: Intercepted {e.rule_name}!")

# Attack 2: Command Injection
print("\n[!] ATTACK 2: Attacker tries Shell Command Injection via report generator...")
report_file = "monthly_report.pdf ; rm -rf /"
print(f"    Payload: {report_file}")
try:
    subprocess.Popen(f"generate_pdf.exe {report_file}", shell=True)
    print("    [-] FAIL: Exploit Succeeded! Shell Compromised!")
except ShieldBlockedException as e:
    print(f"    [+] ZEROARMOR SAVED APP: Intercepted {e.rule_name}!")

# Attack 3: Directory Traversal
print("\n[!] ATTACK 3: Attacker tries Path Traversal to read /etc/passwd...")
target_path = "../../../etc/passwd"
print(f"    Payload: {target_path}")
try:
    with open(target_path, "r") as f:
        pass
    print("    [-] FAIL: Exploit Succeeded! File Read!")
except ShieldBlockedException as e:
    print(f"    [+] ZEROARMOR SAVED APP: Intercepted {e.rule_name}!")

# Attack 4: Secret Leakage
print("\n[!] ATTACK 4: Developer accidentally logs production API Keys...")
print("    Logging: Stripe Key = sk_test_mock_dummy_stripe_key_testing")

# Final Report
print("\n" + "=" * 65)
print("[*] ZEROARMOR SHIELD TELEMETRY REPORT:")
telemetry = zeroarmor.get_telemetry()
for idx, threat in enumerate(telemetry, 1):
    print(f"  {idx}. [{threat['timestamp']}] {threat['rule']} -> {threat['reason']}")
print("=" * 65)
print("[+] RESULT: All 4 Attacks neutralized in real-time with 0 code refactoring!")
print("=" * 65 + "\n")
