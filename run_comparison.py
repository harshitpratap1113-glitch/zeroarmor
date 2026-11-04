"""
ZeroArmor Live Side-by-Side Comparison Runner
Executes:
1. demo_without.py (Without ZeroArmor)
2. demo_with.py (With ZeroArmor)
"""

import subprocess
import sys
import os

folder = os.path.dirname(__file__)

print("\n" + "#" * 65)
print("  [*] ZEROARMOR LIVE COMPARISON: BEFORE VS AFTER DEMO")
print("#" * 65)

# Step 1: Run Without ZeroArmor
print("\n>>> STEP 1: Running application WITHOUT ZeroArmor...")
subprocess.run([sys.executable, os.path.join(folder, "demo_without.py")])

# Step 2: Run With ZeroArmor
print("\n>>> STEP 2: Running the EXACT SAME application WITH 'import zeroarmor'...")
subprocess.run([sys.executable, os.path.join(folder, "demo_with.py")])
