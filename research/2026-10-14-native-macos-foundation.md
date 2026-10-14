# Native macOS foundation for the Omarchy workflow

Researched 2026-10-14. This is a companion to the tool comparison, not a configuration change.

## What is already installed

Read-only inspection of this Mac found macOS 26.7.1 (25G241), BetterTouchTool 6.885, Raycast 2.4.1.0, OmniWM 0.7.6, and Vorssaint 3.4.1 in `/Applications`. These versions came from `sw_vers` and each application's `Contents/Info.plist`, not web release listings. Installed does not establish that every optional feature has company approval or its required permissions.

The live BTT data store contains the preset `omarchy-on-mac-corporate`, with 29 keyboard bindings: 27 enabled and 2 disabled. Fn/Globe is the main modifier, with Shift, Control, and Option used as additional layers. The challenging replacement requirements are both exact Fn chords and moving the current window to a numbered **native Mission Control desktop**.

A `profiles status -type enrollment` check on a corporate Mac is narrow: its result is not evidence that the device is unrestricted, and old project notes about corporate policies should not be treated as a current approval decision.

## Apple already supplies manual window tiling

Apple's macOS 26 guide documents native Window-menu tiling and these shortcuts:

| Action | Apple shortcut |
|---|---|
| Fill the desktop | Fn + Control + F |
| Center | Fn + Control + C |
| Left/right/top/bottom half | Fn + Control + corresponding arrow |
| Return to previous size | Fn + Control + R |
| Arrange two windows horizontally/vertically | Fn + Control + Shift + corresponding arrow |

These are native window operations, not a separate automatic tiling manager. The same guide lists quarter-window menu actions without default keyboard shortcuts. Source: [Apple macOS 26 window tiling icons and keyboard shortcuts](https://support.apple.com/guide/mac-help/mchl9674d0b0/26/mac/26).

Apple also permits changing keyboard shortcuts for categories such as Mission Control in System Settings. Source: [Apple macOS 26 keyboard shortcuts](https://support.apple.com/guide/mac-help/mchlp2262/26/mac/26). Exact acceptance of the user's custom Fn chords in Apple's settings UI was not exercised in this research.

## Spaces are distinct from monitors and third-party workspaces

Apple calls Mission Control desktops **spaces**. Its guide documents Control + Left/Right Arrow for adjacent Space navigation. Moving an app window between Spaces is documented as dragging to an edge or dragging the window to a Space in Mission Control. Assigning an entire application to a desktop using its Dock menu is different from sending an individual current window to a numbered desktop. Source: [Apple macOS 26 multiple Spaces](https://support.apple.com/guide/mac-help/mh14112/26/mac/26).

Consequently, a utility's claim to move a window to the next **screen**, **display**, **monitor**, or its own **workspace** does not establish that it can replace Fn + Shift + 1–4 in this BTT preset. The tool reports evaluate that capability explicitly.

## Apple Shortcuts can cover some app-launch hotkeys

Apple documents adding a keyboard shortcut to a Shortcut and running it from any macOS application. Some system-reserved combinations cannot be overridden. This is a built-in alternative for simple launch and automation actions, but the cited guide does not establish an arbitrary native send-window-to-desktop action or preservation of every custom Fn chord. Source: [Apple run a shortcut while working on your Mac](https://support.apple.com/guide/shortcuts-mac/run-a-shortcut-from-another-app-apd163eb9f95/mac).

## Research limits

No applications were installed, updated, launched for a trial, or configured. No existing BTT bindings were edited. The comparison is documentation and release research; any proposed complete replacement still needs a focused trial of the actual hotkey recorder, Space navigation, and per-window desktop moves on this machine.

Tavily anonymous search reached its shared rate cap; researchers continued through official product sites, tagged source, and release histories. Context7's library resolver did not index the `y3owk1n/mimi` macOS utility; unrelated results were rejected, and mimi claims rely on the author's documentation and release tags rather than a mismatched library.
