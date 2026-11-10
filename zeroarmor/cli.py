"""
ZeroArmor CLI Utility - v2.0 Titanium Edition
Terminal interface to inspect shields, run live diagnostics, stream threat telemetry, and launch the Live Lab.
"""

import sys
import os
import argparse
import json
import time

# Ensure parent directory is at the front of sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    parser = argparse.ArgumentParser(
        prog="zeroarmor",
        description="ZeroArmor Titanium: 32-Vector 1-Line Runtime Application Self-Protection (RASP) Shield."
    )
    parser.add_argument("command", nargs="?", default="status",
                        choices=["status", "test", "version", "info", "monitor", "lab", "export"],
                        help="Action to perform: status, test, version, info, monitor, lab, export")
    parser.add_argument("--json", action="store_true", help="Output status or telemetry in JSON format")
    parser.add_argument("--cef", action="store_true", help="Export telemetry in Common Event Format (CEF)")
    parser.add_argument("--file", type=str, help="Destination file for export")
    parser.add_argument("--port", type=int, default=8899, help="Port for the interactive Live Lab (default: 8899)")

    args = parser.parse_args()

    if args.command == "version":
        print("ZeroArmor v2.0.0 (Titanium Shield Edition)")
        return

    import zeroarmor
    from zeroarmor.core import get_shield

    shield = get_shield()

    if args.command in ["status", "info"]:
        if args.json:
            print(json.dumps(shield.get_status(), indent=2))
        else:
            print("\n" + "=" * 70)
            print("🛡️  ZEROARMOR TITANIUM RASP: 32-VECTOR AUTONOMOUS CYBER DEFENSE")
            print("=" * 70)
            st = shield.get_status()
            version = st.get("version", "2.0.0")
            mode = st.get("mode", "BLOCK")
            print(f"Status:       \033[92m{st['status']}\033[0m")
            print(f"Version:      \033[96mv{version}\033[0m (Titanium Edition)")
            print(f"Defense Mode: \033[93m{mode}\033[0m (Active Neutralization)")
            print(f"Armed Layers: \033[92m{st['active_shields_count']}/{st['total_shields_count']} Defense Shields Active\033[0m")
            print(f"Threats Log:  {st['blocked_attacks_count']} blocked threats recorded")
            print("-" * 70)
            for name, active in st['shields'].items():
                mark = "\033[92m[ACTIVE]\033[0m" if active else "\033[91m[INACTIVE]\033[0m"
                print(f"  {mark:<18} {name}")
            print("=" * 70)
            print("Usage: Just add 'import zeroarmor' at the top of your Python app.\n")

    elif args.command == "test":
        print("\n[*] Running ZeroArmor Titanium 32-Vector In-Memory Diagnostics...")
        import subprocess
        test_file = os.path.join(os.path.dirname(__file__), "..", "tests", "test_32_shields.py")
        if os.path.exists(test_file):
            subprocess.run([sys.executable, test_file])
        else:
            fallback = os.path.join(os.path.dirname(__file__), "..", "tests", "test_20_shields.py")
            subprocess.run([sys.executable, fallback])

    elif args.command == "export":
        if args.cef:
            cef_out = shield.export_telemetry_cef(args.file)
            if not args.file:
                print(cef_out if cef_out else "[*] No threat events recorded yet.")
            else:
                print(f"[+] Exported CEF telemetry to {args.file}")
        else:
            json_out = shield.export_telemetry_json(args.file)
            if not args.file:
                print(json_out if json_out != "[]" else "[*] No threat events recorded yet.")
            else:
                print(f"[+] Exported JSON telemetry to {args.file}")

    elif args.command == "monitor":
        print("\n" + "=" * 70)
        print("🛡️  ZEROARMOR TITANIUM: REAL-TIME THREAT RADAR STREAM")
        print("=" * 70)
        print("[*] Listening for intercepted payloads across all Python processes... (Ctrl+C to stop)\n")
        seen = 0
        try:
            while True:
                events = shield.telemetry
                if len(events) > seen:
                    for ev in events[seen:]:
                        print(f"[{ev['timestamp']}] \033[91mBLOCKED\033[0m {ev['rule']}: {ev['reason']}")
                        print(f"    Payload: \033[90m{ev.get('payload', '')[:100]}\033[0m\n")
                    seen = len(events)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[*] Threat Radar stopped.")

    elif args.command == "lab":
        import subprocess
        lab_script = os.path.join(os.path.dirname(__file__), "..", "live_interactive_lab.py")
        print(f"\n[*] Launching ZeroArmor Titanium Live Interactive Lab on http://127.0.0.1:{args.port} ...")
        subprocess.run([sys.executable, lab_script])

if __name__ == "__main__":
    main()
