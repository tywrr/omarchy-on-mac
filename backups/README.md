# Live settings snapshots

The initial working snapshot is [2026-10-14T191504Z](2026-10-14T191504Z/).
The final central-skhd snapshot is [2026-10-14T204838Z](2026-10-14T204838Z/).
The LocalSend share binding is included in [2026-10-14T234420Z](2026-10-14T234420Z/).
The new-window Ghostty launcher is included in [2026-10-14T235753Z](2026-10-14T235753Z/).
Each directory contains the full WhichSpace preference domain, the full native
symbolic-hotkey preference domain, the active skhd config, and capture metadata.
New snapshots also include the live `toggle-fill.swift` helper source, or a
`NO_PREVIOUS_FILL_HELPER` marker if it was absent. The compiled executable is
derived from the source and is not stored.
Current snapshots also save `com.vorssaint.utils.clipboard-shortcuts.plist` with
only the four clipboard availability/enable/shortcut keys. No clipboard entries
or other Vorssaint preferences are included. The manifest records any keys that
were absent; recovery of that state means deleting those individual keys rather
than importing this partial file as an entire preference domain.

These full exports preserve machine-specific Space/display IDs and unrelated
native shortcuts for recovery on the original Mac. Prefer the portable restore
in the [root README](../README.md) when setting up another Mac: it merges only
the intended shortcuts and selected menu-bar preferences.

Run `python3 scripts/settings.py backup` from the repository root to create
another snapshot and refresh the portable configuration. The restore command
also makes a rollback snapshot before changing live settings. A restore onto a
Mac with no previous skhd config records `NO_PREVIOUS_SKHDRC` instead.

Privacy permissions, login-item approvals, installed applications, and the
creation of Mission Control desktops are outside these preference exports.

For full preference recovery on the same Mac, quit WhichSpace, import the two
saved domains with `defaults import <domain> <snapshot-file>`, restore the saved
`skhdrc` to `~/.config/skhd/skhdrc`, and, when present, copy `toggle-fill.swift`
there and rebuild it with `xcrun swiftc -O ~/.config/skhd/toggle-fill.swift -o ~/.config/skhd/toggle-fill`.
Then relaunch WhichSpace and reload skhd/native
settings. Full imports replace the domain, so use them only when you want that
entire snapshot; take another backup first.

Restore Vorssaint's saved shortcut values individually while the app is stopped,
preserving the rest of its domain, then reopen it. The portable restore performs
that merge automatically. The native helper now also handles full screen, the
Apple menu, and creating new Finder windows.
