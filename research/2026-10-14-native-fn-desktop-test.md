# Native Fn+1–5 desktop switching: verified working

Tested and configured on 2026-10-14 on the user's macOS 26.7.1 Mac.

## Result

**Fn+1, Fn+2, Fn+3, Fn+4 and Fn+5 now switch directly to native Mission Control desktops 1–5.** No Apple Shortcuts entries, standalone hotkey scripts or resident helper are required. BetterTouchTool was not running during the verification; its stored configuration was left unchanged. The user physically tested Fn+2 and Fn+1 and confirmed both work.

## Configuration and verification

The native preference domain is `com.apple.symbolichotkeys`, key `AppleSymbolicHotKeys`. Enabled symbolic actions 118–122 use `type = standard`, digit character codes 49–53, physical keycodes `[18, 19, 20, 21, 23]`, and modifier mask **8388608** (`0x800000`, Fn). The existing native shortcuts were backed up, the five action entries were updated, and Apple's `activateSettings -u` reloaded them. Other shortcut entries were preserved.

A synthetic-key attempt through the native UI recorder did not retain Fn. This does not establish that every physical recorder path rejects Fn; setting the native action's modifier mask directly succeeded.

Runtime verification read the current native Space before and after each synthetic Fn chord:

| Chord | Before Space ID | After Space ID | Target |
|---|---:|---:|---|
| Fn+2 | 1 | 3 | Desktop 2 |
| Fn+3 | 3 | 4 | Desktop 3 |
| Fn+4 | 4 | 5 | Desktop 4 |
| Fn+1 | 5 | 1 | Desktop 1 |
| Fn+5 | 1 | 48 | Desktop 5 |
| Fn+1 | 48 | 1 | Desktop 1 |

There were initially four native desktops. Desktop 5 was added through Mission Control's native Add Desktop button. The test returned to Desktop 1. The final preference export confirmed all five enabled entries retained the Fn modifier mask.

Private SkyLight APIs were used **only to observe active native Space IDs during the test**. The configured keyboard shortcuts are handled by macOS itself. Temporary Python/AppleScript test programs are not installed as background processes or invoked by the hotkeys.

The pre-test native shortcut backup is [native-fn-desktop-test/before.plist](native-fn-desktop-test/before.plist). It reconstructs the initial absence of the Desktop 1 override before the UI-recorder experiment. The trial preference snapshot is also retained in that directory. A full backup import would replace the preference domain, so any later undo should restore only actions 118–122 while preserving subsequent unrelated shortcut changes.

## Limits

- Physical Fn+1 and Fn+2 were confirmed by the user; Fn+3–5 were verified with synthetic events and native Space IDs.
- No logout/reboot persistence test was performed. Values are saved in the native preference domain.
- This verifies desktop **switching**, not sending the focused window to a desktop.
- This does not establish that Apple Shortcuts' generic hotkey recorder supports Fn, or add Fn support to Vorssaint's own shortcut model.
- Existing saved BTT Fn+1–4 shortcuts remain configured. Re-enabling BTT may cause both handlers to compete until those duplicate BTT bindings are disabled.
