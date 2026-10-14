# Fn+Option+F: native Fill toggle

## Result

Super+Option+F is handled by skhd.zig and calls a small compiled Accessibility
helper. It alternates native **Window → Fill** and **Window → Move & Resize →
Return to Previous Size**. It retains Mission Control desktops and macOS's
window-size history. No separate window manager or long-running helper is used.

The source is `skhd/toggle-fill.swift`. Restore installs it in `~/.config/skhd/`
and builds `toggle-fill` using `xcrun swiftc -O`. Backup saves the live source
alongside the live skhdrc and full WhichSpace/native preferences.

## Why a helper

The system keyboard table identifies Fill as symbolic hotkey 237; Center is 238
and Return to Previous Size is 239. Setting 237 to `[102, 3, 8912896]`
(Fn+Option+F), importing the domain, and activating settings did not fire in
either the synthetic or physical test. The user reported “Nothing happens.”
ID 237 was returned to its default Fn+Control+F, `[102, 3, 8650752]`.
Portable restore continues to manage only desktop IDs 118–122.

Clicking Fill twice through the native menu did not toggle: the second call left
the window filled. Return to Previous Size still restored the earlier geometry.
The helper therefore compares the focused window's geometry before and after
Fill. If it did not change, it invokes the native restore command when enabled.
It does not infer Fill merely from the restore menu item's enabled state, which
can also apply to other tiled layouts.

An initial AppleScript helper worked directly but its skhd-launched invocations
waited for Apple Events permissions. That implementation was removed in favor of
direct Accessibility APIs. The compiled helper worked when invoked by the
existing skhd service without an additional permission grant.

## Verification on macOS 26.7.1

Both tests used `skhd --key 'fn + alt - f'`, exercising the installed config,
running event tap, and helper. Coordinates are left, top, right, bottom.

| App | Before | After first press | After second press |
|---|---|---|---|
| Finder test window | 174,150,980,756 | 8,47,1702,1104 | 173,150,980,757 |
| New blank Chrome window | 160,140,1160,840 | 8,47,1702,1104 | 159,140,1160,841 |

The native restore action introduced roughly one pixel of rounding. The Chrome
test window was closed after verification. The user physically confirmed the
final toggle in **Finder, Chrome, Calendar, and Ghostty**. An initial concern
about Ghostty was resolved by the user: its window was already filled.

The Swift source compiled successfully. Backup captured the helper source and
the live config. The full restore flow was exercised on this Mac, rebuilding the
helper, merging the portable settings, restarting WhichSpace, and reloading
skhd. Restore preview then reported no differences against the installed
portable settings. See the timestamped snapshots under `backups/` for rollback.

## Limits

The helper currently uses English menu titles and requires the app to expose
the native Fill and Move & Resize menu commands. Standard desktop windows are
supported; full-screen windows and windows with other Accessibility subroles
are ignored. The helper waits briefly for Fill's geometry update; allow each
press to complete before pressing again.

Apple's documented shortcuts:
https://support.apple.com/guide/mac-help/mchl9674d0b0/26/mac/26
