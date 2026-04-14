#!/usr/bin/env python3
import json
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("site_release_expectations.json")


def load_config():
    return json.loads(CONFIG_PATH.read_text())


def save_config(cfg):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n")


def list_profiles(cfg):
    active = cfg.get("active_profile")
    for name, profile in cfg.get("profiles", {}).items():
        marker = "*" if name == active else " "
        desc = profile.get("description", "")
        print(f"{marker} {name}: {desc}")


def main():
    cfg = load_config()
    args = sys.argv[1:]

    if not args or args[0] in {"-h", "--help", "help"}:
        print("Usage:")
        print("  ./qa/set_active_profile.py list")
        print("  ./qa/set_active_profile.py get")
        print("  ./qa/set_active_profile.py set <profile>")
        sys.exit(0)

    cmd = args[0]
    if cmd == "list":
        list_profiles(cfg)
        return
    if cmd == "get":
        print(cfg.get("active_profile", ""))
        return
    if cmd == "set":
        if len(args) != 2:
            raise SystemExit("Usage: ./qa/set_active_profile.py set <profile>")
        profile_name = args[1]
        if profile_name not in cfg.get("profiles", {}):
            available = ", ".join(sorted(cfg.get("profiles", {}).keys()))
            raise SystemExit(f"Unknown profile: {profile_name}. Available: {available}")
        cfg["active_profile"] = profile_name
        save_config(cfg)
        print(f"active_profile -> {profile_name}")
        return

    raise SystemExit(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
