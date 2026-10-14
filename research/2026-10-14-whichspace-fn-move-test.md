# Direct WhichSpace Fn+Shift+1–5 bindings

Configured on 2026-10-14 for installed **WhichSpace 1.4.1** (`io.gechr.WhichSpace`).

## Source finding

The recorder excludes Fn, but the underlying shortcut representation, stored settings and hotkey API can preserve it. This distinction was missed in the initial research, which correctly identified the recorder limitation but recommended an external dispatcher before testing direct stored bindings.

Release-tag source:

- [Shortcut.swift](https://github.com/gechr/WhichSpace/blob/v1.4.1/Vendor/KeyboardShortcuts/Sources/KeyboardShortcuts/Shortcut.swift): the event/recorder initializer strips `.function`; generic construction preserves semantic Fn for ordinary keys.
- [Utilities.swift](https://github.com/gechr/WhichSpace/blob/v1.4.1/Vendor/KeyboardShortcuts/Sources/KeyboardShortcuts/Utilities.swift): converts Fn to/from Carbon modifier flag **131072** (`0x20000`).
- [HotKey.swift](https://github.com/gechr/WhichSpace/blob/v1.4.1/Vendor/KeyboardShortcuts/Sources/KeyboardShortcuts/HotKey.swift): registers the stored Carbon modifier flags through `RegisterEventHotKey`.
- [Hotkeys.swift](https://github.com/gechr/WhichSpace/blob/v1.4.1/WhichSpace/Hotkeys.swift): numbered `moveToSpace1`–`moveToSpace16` actions are distinct from send-only actions.

A temporary native API probe successfully registered and unregistered Fn+Shift+5 with status **0**, without changing app settings.

## Applied change

Backed up WhichSpace preferences, briefly stopped the menu-bar app, changed **only** `KeyboardShortcuts_moveToSpace1`–`KeyboardShortcuts_moveToSpace5`, then relaunched `/Applications/WhichSpace.app`.

Each value is a JSON string containing:

- `carbonModifiers = 131584` = Fn **131072** + Shift **512**.
- `carbonKeyCode = 18, 19, 20, 21, 23` for digits 1–5.

The subsequent preference export confirmed exactly those five keys changed. All other settings, including menu-bar appearance, remained unchanged. The native Fn+1–5 desktop-switch bindings were not modified. No Shortcuts entries, runtime scripts or additional hotkey applications were created for this solution.

Before this change, Move to Space 1–3 used Control+Shift+number (`carbonModifiers = 4608`); 4–5 were unset.

**Move follows the transferred window.** The separate Send actions would leave the user on the original desktop. This matches the user's successful existing Control+Shift Move test.

## Verification status

- macOS accepted a temporary Fn+Shift+5 registration using the same native API as WhichSpace.
- All five stored values were verified after WhichSpace restarted.
- **The user physically tested Fn+Shift+2 and Fn+Shift+1 and confirmed both move the focused window and follow it to the destination desktop.** Fn+Shift+3–5 use the same verified configuration pattern; those three physical chords were not separately reported as tested.
- AppleScript read/export requests timed out during this investigation; the applied path does not depend on AppleScript or Shortcuts.

## Backup and maintenance

- [Full pre-change preferences](whichspace-fn-move-test/before.plist).
- [Original five hotkey values](whichspace-fn-move-test/before-hotkeys.json).
- [Configured five hotkey values](whichspace-fn-move-test/configured-hotkeys.json).

WhichSpace's recorder still strips Fn, so re-recording these bindings can remove it. The imported/stored values and recorder behavior should be rechecked after future app changes. Existing BTT Fn+Shift bindings remain saved but BTT was not running at the preceding check; running both input handlers could create conflicts.

To undo later, restore only the five affected keys from the backup while WhichSpace is stopped and then relaunch it, preserving subsequent unrelated changes. A full preference-domain import would replace later settings as well.
