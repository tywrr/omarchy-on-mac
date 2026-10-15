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

from install_panel import APP as PANEL_APP, PDF_NAMES, install as install_panel, needs_install as panel_needs_install


ROOT = Path(__file__).resolve().parents[1]
LIVE_SKHD = Path.home() / ".config/skhd/skhdrc"
HELPER_NAME = "toggle-fill.swift"
LIVE_HELPER = LIVE_SKHD.parent / HELPER_NAME
LIVE_HELPER_BINARY = LIVE_SKHD.parent / "toggle-fill"
WHICHSPACE = "io.gechr.WhichSpace"
SYMBOLIC = "com.apple.symbolichotkeys"
VORSSAINT = "com.vorssaint.utils"
VORSSAINT_KEYS = {
    "featureAvailable.clipboardHistory": True,
    "clipboardHistoryEnabled": True,
    "clipboardHistoryShortcutEnabled": True,
    "clipboardHistoryShortcut": "control+option+command:9",
}
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


def clipboard_preferences():
    # Never save the complete domain: it can contain legacy clipboard history.
    preferences = export_preferences(VORSSAINT)
    return {key: preferences[key] for key in VORSSAINT_KEYS if key in preferences}


def stop_app_if_running(process_name, bundle_id):
    result = subprocess.run(["/usr/bin/pgrep", "-x", process_name], capture_output=True)
    if result.returncode == 1:
        return False
    if result.returncode != 0:
        raise RuntimeError(f"Could not determine whether {process_name} is running")
    run([
        "/usr/bin/osascript", "-e",
        f'with timeout of 5 seconds\ntell application id "{bundle_id}" to quit\nend timeout',
    ], timeout=8)
    deadline = time.monotonic() + 3
    while subprocess.run(["/usr/bin/pgrep", "-x", process_name], capture_output=True).returncode == 0:
        if time.monotonic() >= deadline:
            raise RuntimeError(f"{process_name} did not exit; settings were not imported")
        time.sleep(0.1)
    return True


def snapshot(output=None, refresh=False):
    stamp = datetime.datetime.now(datetime.timezone.utc)
    directory = output or ROOT / "backups" / stamp.strftime("%Y-%m-%dT%H%M%SZ")
    whichspace = export_preferences(WHICHSPACE)
    symbolic = export_preferences(SYMBOLIC)
    vorssaint = clipboard_preferences()
    skhd = LIVE_SKHD.read_bytes() if LIVE_SKHD.exists() else None
    helper = LIVE_HELPER.read_bytes() if LIVE_HELPER.exists() else None
    panel_resources = PANEL_APP / "Contents/Resources"
    panel_present = (PANEL_APP / "Contents/MacOS/OmarchyKeys").exists()
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
    save_plist(directory / f"{VORSSAINT}.clipboard-shortcuts.plist", vorssaint)
    if skhd is None:
        (directory / "NO_PREVIOUS_SKHDRC").touch()
    else:
        (directory / "skhdrc").write_bytes(skhd)
    if helper is None:
        (directory / "NO_PREVIOUS_FILL_HELPER").touch()
    else:
        (directory / HELPER_NAME).write_bytes(helper)
    if panel_present:
        panel_backup = directory / "keys-panel"
        panel_backup.mkdir()
        shutil.copyfile(PANEL_APP / "Contents/Info.plist", panel_backup / "Info.plist")
        for name in ("OmarchyKeys.swift", "build.sha256", *PDF_NAMES):
            shutil.copyfile(panel_resources / name, panel_backup / name)
    else:
        (directory / "NO_PREVIOUS_KEYS_PANEL").touch()
    (directory / "manifest.json").write_text(
        json.dumps(
            {
                "captured_at_utc": stamp.isoformat(),
                "skhd_config_source": "~/.config/skhd/skhdrc",
                "skhd_config_present": skhd is not None,
                "fill_helper_source": f"~/.config/skhd/{HELPER_NAME}",
                "fill_helper_present": helper is not None,
                "keys_panel_present": panel_present,
                "keys_panel_app": "~/Applications/Omarchy Keys.app",
                "keys_panel_scope": "Source, bundle metadata, and PDFs; no compiled executable or search history.",
                "preference_domains": [WHICHSPACE, SYMBOLIC],
                "vorssaint_shortcut_keys": list(VORSSAINT_KEYS),
                "vorssaint_keys_absent": [key for key in VORSSAINT_KEYS if key not in vorssaint],
                "vorssaint_scope": "Clipboard shortcut configuration only; no history or content.",
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
        save_plist(ROOT / "vorssaint/settings.plist", {
            key: vorssaint.get(key, default) for key, default in VORSSAINT_KEYS.items()
        })
        save_plist(
            ROOT / "macos/desktop-shortcuts.plist",
            {"AppleSymbolicHotKeys": {key: native_hotkeys[key] for key in DESKTOP_IDS}},
        )
    print(f"Backup: {directory}")
    if refresh:
        print("Refreshed skhd config/helper, WhichSpace, Vorssaint shortcuts, and native desktops")
    return directory


def load_portable_settings():
    whichspace = plistlib.loads((ROOT / "whichspace/settings.plist").read_bytes())
    symbolic = plistlib.loads((ROOT / "macos/desktop-shortcuts.plist").read_bytes())
    skhd = (ROOT / "skhd/skhdrc").read_bytes()
    helper = (ROOT / "skhd" / HELPER_NAME).read_bytes()
    vorssaint = plistlib.loads((ROOT / "vorssaint/settings.plist").read_bytes())
    if not isinstance(vorssaint, dict) or set(vorssaint) != set(VORSSAINT_KEYS) or any(
        type(vorssaint[key]) is not type(default) for key, default in VORSSAINT_KEYS.items()
    ):
        raise ValueError("Vorssaint settings must contain only the four clipboard shortcut keys")
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
    return whichspace, hotkeys, skhd, helper, vorssaint


def restore(dry_run):
    desired_whichspace, desired_hotkeys, desired_skhd, desired_helper, desired_vorssaint = load_portable_settings()
    current_whichspace = export_preferences(WHICHSPACE)
    current_symbolic = export_preferences(SYMBOLIC)
    current_vorssaint = clipboard_preferences()
    vorssaint_changes = [
        key for key, value in desired_vorssaint.items() if current_vorssaint.get(key) != value
    ]
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
    panel_changes = panel_needs_install()
    print(f"skhd config differs: {config_changes}")
    print(f"Fill helper differs: {helper_changes}")
    print(f"Shortcut panel differs: {panel_changes}")
    print(f"WhichSpace keys to change: {whichspace_changes}")
    print(f"Vorssaint clipboard shortcut keys to change: {vorssaint_changes}")
    print(f"Native desktop shortcut IDs to change: {native_changes}")
    print("Other native hotkeys and WhichSpace's machine-specific preferences are preserved.")
    if dry_run:
        print("Dry run: no files, preferences, or processes changed.")
        return

    # Preserve the entire previous state, including an absent skhd config.
    snapshot()

    # Build the local UI before changing the shortcuts that summon it.
    if panel_changes:
        install_panel()

    # Compile before changing preferences. The binary is derived from the saved
    # source; only the source is portable and tracked in git.
    LIVE_SKHD.parent.mkdir(parents=True, exist_ok=True)
    if helper_changes:
        with tempfile.TemporaryDirectory(prefix="omarchy-fill-build-") as directory:
            source = Path(directory) / HELPER_NAME
            binary = Path(directory) / "toggle-fill"
            source.write_bytes(desired_helper)
            try:
                run(["/usr/bin/xcrun", "swiftc", "-O", str(source), "-o", str(binary)])
            except subprocess.CalledProcessError as error:
                raise RuntimeError(error.stderr.decode().strip()) from error
            binary.replace(LIVE_HELPER_BINARY)

    was_running = False
    vorssaint_was_running = False
    try:
        if whichspace_changes:
            was_running = stop_app_if_running("WhichSpace", WHICHSPACE)
        if vorssaint_changes:
            vorssaint_was_running = stop_app_if_running("Vorssaint", VORSSAINT)
        # Read again after quitting so any settings saved on exit are retained.
        merged_whichspace = export_preferences(WHICHSPACE)
        merged_whichspace.update(desired_whichspace)
        merged_symbolic = export_preferences(SYMBOLIC)
        merged_symbolic.setdefault("AppleSymbolicHotKeys", {}).update(desired_hotkeys)
        import_preferences(WHICHSPACE, merged_whichspace)
        import_preferences(SYMBOLIC, merged_symbolic)
        for key in vorssaint_changes:
            value = desired_vorssaint[key]
            flag = "-bool" if isinstance(value, bool) else "-string"
            text = str(value).lower() if isinstance(value, bool) else value
            run(["/usr/bin/defaults", "write", VORSSAINT, key, flag, text])
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
        if vorssaint_was_running:
            run(["/usr/bin/open", "-b", VORSSAINT])

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
