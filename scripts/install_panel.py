#!/usr/bin/env python3
"""Build the native shortcut panel into ~/Applications/Omarchy Keys.app."""

import argparse
import hashlib
import os
from pathlib import Path
import platform
import plistlib
import shutil
import signal
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
APP = Path.home() / "Applications/Omarchy Keys.app"
PDF_NAMES = ("omarchy-on-mac-keybindings-dark.pdf", "herdr-keybindings-omarchy-dark.pdf")
INPUTS = [ROOT / "panel/OmarchyKeys.swift", ROOT / "panel/Info.plist"] + [
    ROOT / "output/pdf" / name for name in PDF_NAMES
]


def fingerprint():
    digest = hashlib.sha256(platform.machine().encode())
    for path in INPUTS:
        digest.update(str(path.relative_to(ROOT)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest() + "\n"


def needs_install():
    receipt = APP / "Contents/Resources/build.sha256"
    return not (
        (APP / "Contents/MacOS/OmarchyKeys").exists()
        and receipt.exists() and receipt.read_text() == fingerprint()
    )


def install():
    if not needs_install():
        print(f"Shortcut panel is current: {APP}")
        return
    if APP.exists():
        info = plistlib.loads((APP / "Contents/Info.plist").read_bytes())
        if info.get("CFBundleIdentifier") != "local.omarchy.keys":
            raise ValueError(f"Refusing to replace an unrelated app at {APP}")
    APP.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".omarchy-keys-build-", dir=APP.parent) as directory:
        staging = Path(directory) / APP.name
        executable = staging / "Contents/MacOS/OmarchyKeys"
        resources = staging / "Contents/Resources"
        executable.parent.mkdir(parents=True)
        resources.mkdir()
        shutil.copyfile(INPUTS[1], staging / "Contents/Info.plist")
        shutil.copyfile(INPUTS[0], resources / "OmarchyKeys.swift")
        for name in PDF_NAMES:
            shutil.copyfile(ROOT / "output/pdf" / name, resources / name)
        (resources / "build.sha256").write_text(fingerprint())
        subprocess.run(["/usr/bin/xcrun", "swiftc", "-O", str(INPUTS[0]), "-o", str(executable)], check=True)
        subprocess.run(["/usr/bin/codesign", "--force", "--sign", "-", str(staging)], check=True)

        # Stop only this helper. The next hotkey launches the updated app.
        running = subprocess.run(["/usr/bin/pgrep", "-x", "OmarchyKeys"], capture_output=True, text=True)
        if running.returncode not in (0, 1):
            raise RuntimeError("Could not check the running shortcut panel")
        for pid in running.stdout.split():
            try:
                os.kill(int(pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
        previous = Path(directory) / "previous.app"
        if APP.exists():
            APP.rename(previous)
        try:
            staging.rename(APP)
        except OSError:
            if previous.exists():
                previous.rename(APP)
            raise
    print(f"Installed shortcut panel: {APP}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    if arguments.dry_run:
        print(f"Shortcut panel differs: {needs_install()}")
    else:
        install()
