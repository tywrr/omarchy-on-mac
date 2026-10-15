# Research and implementation notes

The current stack is **skhd.zig + WhichSpace + native macOS desktops**, with
Fn/Globe as Super. The [root README](../README.md) and tracked configs describe
the current setup. Earlier reports are dated research snapshots; recommendations
and unresolved questions in them may predate the subsequent working setup.

## Working configuration

- [Central skhd routing](2026-10-14-central-skhd-routing.md): current Fn map;
  native Control+1–5, WhichSpace Control+Shift+1–5, clipboard, and system actions.
- [Native Fill toggle](2026-10-14-native-fill-toggle.md): Fn+Option+F;
  skhd plus a compiled native helper, verified with synthetic presses in Finder and Chrome.
- [skhd app launches](2026-10-14-skhd-app-launches.md): six launch actions;
  synthetic events verified, physical-key confirmation pending.
- [Native Fn desktop switching](2026-10-14-native-fn-desktop-test.md): earlier
  direct native configuration; Fn routing has since moved into skhd.
- [WhichSpace window moves](2026-10-14-whichspace-fn-move-test.md): earlier direct
  Fn configuration; skhd now forwards to ordinary WhichSpace shortcuts.

The small directories alongside these reports preserve their pre-change trial
preferences. The separate [backups](../backups/) directory contains the full
current working snapshot.

## Alternatives and native capabilities

- [Searchable shortcut windows](2026-10-14-searchable-shortcut-viewers-third-party.md):
  native PDF panels, KeyClu, and alternatives for the macOS and Herdr sheets.
- [Hotkey tools](2026-10-14-hotkey-tools.md)
- [Native macOS foundation](2026-10-14-native-macos-foundation.md)
- [Native window and desktop transfers](2026-10-14-native-window-desktop-transfers.md)
- [Window tools](2026-10-14-native-window-tools.md)
- [Vorssaint deep dive](2026-10-14-vorssaint-deep-dive.md)
- [OmniWM and Omarchy stacks](2026-10-14-omniwm-and-omarchy-stacks.md)
- [Integrated and Spaces tools](2026-10-14-integrated-and-spaces-tools.md)
- [macOS 26 versus 27](2026-10-14-native-macos-26-vs-27.md)
- [Original BTT alternatives overview](2026-10-14-btt-alternatives.md)
