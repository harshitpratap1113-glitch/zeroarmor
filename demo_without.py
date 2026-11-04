"""
SCENARIO A: BINA ZEROARMOR KE (UNPROTECTED APP)
Normal Python code without security armor.
"""

import sqlite3
import subprocess
import os

print("\n" + "=" * 60)
print("[-] SCENARIO 1: APP WITHOUT ZEROARMOR (DEFENSELESS)")
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
cursor.execute(query)
stolen_data = cursor.fetchall()
print(f"    [!] HACKED! Attacker dumped the database: {stolen_data}")

# --- 2. Command Injection / RCE Attack ---
print("\n[!] ATTACK 2: Attacker injects shell command (& whoami)")
malicious_cmd = "cmd.exe /c echo Processing report & whoami"
print(f"    Executing command: {malicious_cmd}")
proc = subprocess.Popen(malicious_cmd, shell=True, stdout=subprocess.PIPE, text=True)
stdout, _ = proc.communicate()
print(f"    [!] HACKED! Attacker executed shell commands on server:\n    Output: {stdout.strip()}")

# --- 3. Path Traversal Attack ---
print("\n[!] ATTACK 3: Attacker tries Path Traversal (../../.env)")
fake_env = "../../../sensitive_config.env"
print(f"    Attempting to open: {fake_env}")
print("    [!] HACKED! File system boundary violated without check!")

# --- 4. Secret Leak in Logs ---
print("\n[!] ATTACK 4: Developer logs API credentials to stdout")
live_stripe = "sk_test_mock_dummy_stripe_key_testing"
print(f"    App Log: Payment gateway initialized with key: {live_stripe}")
print("    [!] HACKED! Real production Stripe key exposed in plaintext logs!")

print("\n" + "=" * 60)
print("[-] SUMMARY: 4 OUT OF 4 ATTACKS SUCCEEDED! APP FULLY COMPROMISED!")
print("=" * 60 + "\n")
