#!/usr/bin/env python3
"""Back up the working setup and restore its portable settings on macOS."""

import argparse
import datetime
import json
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
LIVE_SKHD = Path.home() / ".config/skhd/skhdrc"
HELPER_NAME = "toggle-fill.swift"
LIVE_HELPER = LIVE_SKHD.parent / HELPER_NAME
LIVE_HELPER_BINARY = LIVE_SKHD.parent / "toggle-fill"
WHICHSPACE = "io.gechr.WhichSpace"
SYMBOLIC = "com.apple.symbolichotkeys"
DESKTOP_IDS = tuple(str(value) for value in range(118, 123))
# Deliberately omit Space/display UUIDs, window positions, and updater state.
APPEARANCE_KEYS = {"clickToSwitchSpaces", "hideEmptySpaces", "showAllSpaces"}


def run(args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, **kwargs)


def export_preferences(domain):
    result = subprocess.run(
        ["/usr/bin/defaults", "export", domain, "-"], capture_output=True
    )
    if result.returncode:
        if b"does not exist" in result.stderr.lower():
            return {}
        raise RuntimeError(result.stderr.decode().strip())
    return plistlib.loads(result.stdout)


def save_plist(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(plistlib.dumps(value, fmt=plistlib.FMT_XML, sort_keys=True))


def import_preferences(domain, value):
    with tempfile.TemporaryDirectory(prefix="omarchy-on-mac-") as directory:
        path = Path(directory) / "preferences.plist"
        save_plist(path, value)
        run(["/usr/bin/defaults", "import", domain, str(path)])


def snapshot(output=None, refresh=False):
    stamp = datetime.datetime.now(datetime.timezone.utc)
    directory = output or ROOT / "backups" / stamp.strftime("%Y-%m-%dT%H%M%SZ")
    whichspace = export_preferences(WHICHSPACE)
    symbolic = export_preferences(SYMBOLIC)
    skhd = LIVE_SKHD.read_bytes() if LIVE_SKHD.exists() else None
    helper = LIVE_HELPER.read_bytes() if LIVE_HELPER.exists() else None
    native_hotkeys = symbolic.get("AppleSymbolicHotKeys", {})
    if refresh:
        if skhd is None:
            raise RuntimeError(f"No live skhd config at {LIVE_SKHD}")
        if helper is None:
            raise RuntimeError(f"No live Fill helper at {LIVE_HELPER}")
        missing = [key for key in DESKTOP_IDS if key not in native_hotkeys]
        if missing:
            raise RuntimeError(f"Desktop shortcut IDs missing: {', '.join(missing)}")
    directory.mkdir(parents=True, exist_ok=False)
    save_plist(directory / f"{WHICHSPACE}.plist", whichspace)
    save_plist(directory / f"{SYMBOLIC}.plist", symbolic)
    if skhd is None:
        (directory / "NO_PREVIOUS_SKHDRC").touch()
    else:
        (directory / "skhdrc").write_bytes(skhd)
    if helper is None:
        (directory / "NO_PREVIOUS_FILL_HELPER").touch()
    else:
        (directory / HELPER_NAME).write_bytes(helper)
    (directory / "manifest.json").write_text(
        json.dumps(
            {
                "captured_at_utc": stamp.isoformat(),
                "skhd_config_source": "~/.config/skhd/skhdrc",
                "skhd_config_present": skhd is not None,
                "fill_helper_source": f"~/.config/skhd/{HELPER_NAME}",
                "fill_helper_present": helper is not None,
                "preference_domains": [WHICHSPACE, SYMBOLIC],
                "scope": "Full preference snapshots; Space/display IDs are machine-specific.",
            },
            indent=2,
        )
        + "\n"
    )
    if refresh:
        (ROOT / "skhd").mkdir(exist_ok=True)
        (ROOT / "skhd/skhdrc").write_bytes(skhd)
        (ROOT / "skhd" / HELPER_NAME).write_bytes(helper)
        portable_whichspace = {
            key: value
            for key, value in whichspace.items()
            if key.startswith("KeyboardShortcuts_") or key in APPEARANCE_KEYS
        }
        save_plist(ROOT / "whichspace/settings.plist", portable_whichspace)
        save_plist(
            ROOT / "macos/fn-desktops.plist",
            {"AppleSymbolicHotKeys": {key: native_hotkeys[key] for key in DESKTOP_IDS}},
        )
    print(f"Backup: {directory}")
    if refresh:
        print("Refreshed skhd config/helper, whichspace/settings.plist, macos/fn-desktops.plist")
    return directory


def load_portable_settings():
    whichspace = plistlib.loads((ROOT / "whichspace/settings.plist").read_bytes())
    symbolic = plistlib.loads((ROOT / "macos/fn-desktops.plist").read_bytes())
    skhd = (ROOT / "skhd/skhdrc").read_bytes()
    helper = (ROOT / "skhd" / HELPER_NAME).read_bytes()
    if not isinstance(whichspace, dict) or any(
        not key.startswith("KeyboardShortcuts_") and key not in APPEARANCE_KEYS
        for key in whichspace
    ):
        raise ValueError("WhichSpace portable settings contain unexpected keys")
    hotkeys = symbolic.get("AppleSymbolicHotKeys", {})
    if set(symbolic) != {"AppleSymbolicHotKeys"} or set(hotkeys) != set(DESKTOP_IDS):
        raise ValueError("Native settings must contain only desktop shortcut IDs 118–122")
    if not skhd.strip():
        raise ValueError("Repository skhd config is empty")
    if not helper.strip():
        raise ValueError("Repository Fill helper is empty")
    return whichspace, hotkeys, skhd, helper


def restore(dry_run):
    desired_whichspace, desired_hotkeys, desired_skhd, desired_helper = load_portable_settings()
    current_whichspace = export_preferences(WHICHSPACE)
    current_symbolic = export_preferences(SYMBOLIC)
    current_hotkeys = current_symbolic.get("AppleSymbolicHotKeys", {})
    whichspace_changes = [
        key for key, value in desired_whichspace.items() if current_whichspace.get(key) != value
    ]
    native_changes = [
        key for key, value in desired_hotkeys.items() if current_hotkeys.get(key) != value
    ]
    config_changes = not LIVE_SKHD.exists() or LIVE_SKHD.read_bytes() != desired_skhd
    helper_changes = (
        not LIVE_HELPER.exists() or LIVE_HELPER.read_bytes() != desired_helper
        or not LIVE_HELPER_BINARY.exists()
    )
    print(f"skhd config differs: {config_changes}")
    print(f"Fill helper differs: {helper_changes}")
    print(f"WhichSpace keys to change: {whichspace_changes}")
    print(f"Native desktop shortcut IDs to change: {native_changes}")
    print("Other native hotkeys and WhichSpace's machine-specific preferences are preserved.")
    if dry_run:
        print("Dry run: no files, preferences, or processes changed.")
        return

    # Preserve the entire previous state, including an absent skhd config.
    snapshot()

    # Compile before changing preferences. The binary is derived from the saved
    # source; only the source is portable and tracked in git.
    LIVE_SKHD.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="omarchy-fill-build-") as directory:
        source = Path(directory) / HELPER_NAME
        binary = Path(directory) / "toggle-fill"
        source.write_bytes(desired_helper)
        try:
            run(["/usr/bin/xcrun", "swiftc", "-O", str(source), "-o", str(binary)])
        except subprocess.CalledProcessError as error:
            raise RuntimeError(error.stderr.decode().strip()) from error
        binary.replace(LIVE_HELPER_BINARY)

    running = subprocess.run(
        ["/usr/bin/pgrep", "-x", "WhichSpace"], capture_output=True
    )
    if running.returncode not in (0, 1):
        raise RuntimeError("Could not determine whether WhichSpace is running")
    was_running = running.returncode == 0
    if was_running:
        run(
            [
                "/usr/bin/osascript", "-e",
                'with timeout of 5 seconds\n'
                'tell application id "io.gechr.WhichSpace" to quit\n'
                'end timeout',
            ],
            timeout=8,
        )
        deadline = time.monotonic() + 3
        while subprocess.run(["/usr/bin/pgrep", "-x", "WhichSpace"], capture_output=True).returncode == 0:
            if time.monotonic() >= deadline:
                raise RuntimeError("WhichSpace did not exit; settings were not imported")
            time.sleep(0.1)

    try:
        # Read again after quitting so any settings saved on exit are retained.
        merged_whichspace = export_preferences(WHICHSPACE)
        merged_whichspace.update(desired_whichspace)
        merged_symbolic = export_preferences(SYMBOLIC)
        merged_symbolic.setdefault("AppleSymbolicHotKeys", {}).update(desired_hotkeys)
        import_preferences(WHICHSPACE, merged_whichspace)
        import_preferences(SYMBOLIC, merged_symbolic)
        LIVE_SKHD.parent.mkdir(parents=True, exist_ok=True)
        LIVE_SKHD.write_bytes(desired_skhd)
        LIVE_HELPER.write_bytes(desired_helper)
        run([
            "/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings",
            "-u",
        ])
    finally:
        if was_running:
            run(["/usr/bin/open", "-a", "WhichSpace"])

    skhd_binary = shutil.which("skhd")
    if skhd_binary:
        result = subprocess.run([skhd_binary, "--reload"], capture_output=True, text=True)
        if result.returncode:
            print("Settings restored. Start skhd with: skhd --start-service")
        else:
            print(result.stdout.strip())
    else:
        print("Settings restored. Install/start skhd.zig to use the app hotkeys.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    backup = commands.add_parser("backup", help="Snapshot live settings and refresh portable configs")
    backup.add_argument("--output", type=Path, help="New directory for the full snapshot")
    apply = commands.add_parser("restore", help="Merge portable settings and copy the skhd config")
    apply.add_argument("--dry-run", action="store_true", help="Show differences without making changes")
    args = parser.parse_args()
    if sys.platform != "darwin":
        parser.error("This tool requires macOS")
    if args.command == "backup":
        snapshot(args.output, refresh=True)
    else:
        restore(args.dry_run)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
