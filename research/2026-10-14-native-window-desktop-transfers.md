# Fn+Shift+1–5: sending windows to native desktops

**Verified follow-up:** installed WhichSpace 1.4.1 now handles **Fn+Shift+1–5 directly**, through its saved hotkey settings. The recorder strips Fn, but its underlying representation and engine preserve it. The user physically confirmed Fn+Shift+1/Fn+Shift+2 move the window and follow it. No external dispatcher or script is needed. See [configuration and evidence](2026-10-14-whichspace-fn-move-test.md). The native-only analysis below remains relevant, but its WhichSpace dispatcher requirement is superseded.

Investigated 2026-10-14 after native Fn+1–5 desktop switching was configured and verified. No window-transfer bindings, helper installations or permission changes were made in this follow-up.

## Finding

No exposed built-in symbolic action for **send the focused window to Desktop N** was found. This is supported by the installed KeyboardSettings action table, its English localization strings, and Apple's Spaces guide. It is a limited negative finding, not proof that no undocumented internal action could exist.

The symbolic preference domain rebinds predefined actions; an invented ID cannot define a new window-transfer operation. Adding Shift to the existing Desktop 1 action would change its trigger, not transform desktop switching into window movement. Similarly, the native **Move left/right a space** labels refer to desktop navigation.

The modifier representation is not the obstacle: Fn+Shift can be represented by mask 8519680. What is missing is an established native transfer action to bind it to.

## Options

| Option | Native Apple desktops? | Exact one-chord Fn+Shift+N? | Practical scope |
|---|---|---|---|
| Mission Control window dragging | Yes | No | Supported native manual method; no helper needed. |
| Hold a title bar while using the existing Fn+N desktop shortcut | Yes | Mouse-assisted | Common native workaround; not tested on this Mac in this follow-up. |
| Custom AppleScript/Shortcuts UI automation | Yes | Dispatcher still needs verification | Could automate grabbing a title bar, switching desktop, releasing the window; title-bar geometry, timing, multiple displays and exact Fn hotkey recording require testing. No public direct window-to-desktop command was established. |
| Existing BTT for only these five bindings | Yes | BTT already has Fn+Shift+1–4 configured | Smallest change; add Desktop 5, preserve native Fn+1–5 desktop switching, and remove BTT's duplicate desktop-switch bindings before running both. No BTT changes made here. |
| WhichSpace plus a verified Fn-capable hotkey dispatcher | Yes | Via integration | WhichSpace v1.4.1 provides numbered Send (stay) and Move (follow), with Shortcuts/AppleScript/URL interfaces. Its own recorder strips Fn. Current Raycast documentation describes Fn bindings, but the installed version/integration still needs verification. |
| Custom helper using private Apple window-server APIs | Yes | With its own event handler | Technically another development route, not a supported native setting; must handle permissions, window selection, OS compatibility and hotkey ownership. Prefer maintained helpers unless custom implementation is itself desired. |

Creating Apple Shortcuts entries alone does not supply a missing native window-transfer action. They can host a UI-automation script or invoke a helper's provided action. Native desktop switching remains configured independently and needs no script.

## Sources checked

- Installed action definitions: `/System/Library/ExtensionKit/Extensions/KeyboardSettings.appex/Contents/Resources/en_GB.lproj/DefaultShortcutsTable.xml`.
- Installed English labels: `/System/Library/ExtensionKit/Extensions/KeyboardSettings.appex/Contents/Resources/DefaultShortcutsTable.loctable`, `en` dictionary. It includes Switch to Desktop 1–16 and Move left/right a space; no window-to-numbered-desktop label was found.
- [Apple: Work in multiple Spaces, macOS 26](https://support.apple.com/guide/mac-help/mh14112/26/mac/26).
- [WhichSpace v1.4.1 documentation](https://github.com/gechr/WhichSpace/blob/v1.4.1/README.md): automation, numbered Send/Move, movement compatibility Sonoma or Tahoe26.4+, unsupported Sequoia.
- [Raycast hotkey documentation](https://manual.raycast.com/command-aliases-and-hotkeys), reviewed in the preceding investigation; installed-version parity remains untested.
- [Mouse-assisted native workaround discussion](https://apple.stackexchange.com/questions/1488/how-to-move-a-window-to-another-space-without-using-the-mouse): historical community evidence, not current Apple support or a live verification.

Related: [verified native Fn+1–5 switching](2026-10-14-native-fn-desktop-test.md), [native macOS comparison](2026-10-14-native-macos-26-vs-27.md), [native-desktop helpers](2026-10-14-integrated-and-spaces-tools.md).
