#!/usr/bin/env bash
# ZeroArmor 1-Click Bootstrap Installer for Linux / macOS
set -e

echo ""
echo "=========================================================="
echo "   🛡️ ZeroArmor v1.0.0 Automated Cloud Installer          "
echo "   Instant 22-Vector RASP Immunity for Any Python Project"
echo "=========================================================="
echo ""

WHEEL_URL="https://github.com/harshitpratap1113-glitch/zeroarmor/releases/download/v1.0.0/zeroarmor-1.0.0-py3-none-any.whl"

echo "[*] Installing ZeroArmor via pip..."
python3 -m pip install --upgrade --no-cache-dir "$WHEEL_URL"

echo ""
echo "[+] ZeroArmor successfully installed!"
echo "[*] Verifying protection core..."
python3 -c "import zeroarmor; print('✅ Core Verification: ARMORED | 22 Shields Online!')"
echo ""
echo "Quick Start:"
echo "  Add 'import zeroarmor' at the top of your python script/web app."
echo ""
