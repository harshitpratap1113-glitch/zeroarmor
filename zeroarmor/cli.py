"""
ZeroArmor CLI Utility
Allows developers to verify shield status and test defense layers from the terminal.
"""

import sys
import argparse
import json

def main():
    parser = argparse.ArgumentParser(
        prog="zeroarmor",
        description="ZeroArmor: 22-Vector 1-Line Runtime Application Self-Protection (RASP) Shield."
    )
    parser.add_argument("command", nargs="?", default="status", choices=["status", "test", "version", "info"],
                        help="Action to perform: status, test, version, info")
    parser.add_argument("--json", action="store_true", help="Output status in JSON format")

    args = parser.parse_args()

    if args.command == "version":
        print("ZeroArmor v1.0.0 (Community Edition)")
        return

    import zeroarmor
    from zeroarmor.core import get_shield

    shield = get_shield()

    if args.command in ["status", "info"]:
        if args.json:
            print(json.dumps(shield.get_status(), indent=2))
        else:
            print("\n" + "=" * 65)
            print("🛡️  ZEROARMOR CYBER DEFENSE: 22-VECTOR RASP SHIELD")
            print("=" * 65)
            st = shield.get_status()
            print(f"Status:       \033[92m{st['status']}\033[0m")
            print(f"Armed Layers: \033[92m{st['active_shields_count']}/{st['total_shields_count']} Defense Shields Active\033[0m")
            print(f"Threats Log:  {st['blocked_attacks_count']} blocked threats recorded")
            print("-" * 65)
            for name, active in st['shields'].items():
                mark = "\033[92m[ACTIVE]\033[0m" if active else "\033[91m[INACTIVE]\033[0m"
                print(f"  {mark:<18} {name}")
            print("=" * 65)
            print("Just add 'import zeroarmor' at the top of your Python app.\n")

    elif args.command == "test":
        print("\n[*] Running ZeroArmor In-Memory Self-Diagnostic...")
        from ..tests.test_20_shields import (
            test_sql_injection_armor,
            test_command_injection_armor,
            test_path_traversal_armor,
            test_ssrf_metadata_armor,
            test_deserialization_armor
        )
        test_sql_injection_armor()
        test_command_injection_armor()
        test_path_traversal_armor()
        test_ssrf_metadata_armor()
        test_deserialization_armor()
        print("\n✅ All core shields verified operational!\n")

if __name__ == "__main__":
    main()
