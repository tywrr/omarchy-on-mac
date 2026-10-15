# Central Fn routing through skhd.zig

Date: 2026-10-14. Tested on macOS 26.7.1 with skhd.zig 0.2.0-7e95d99,
WhichSpace 1.4.1, and Vorssaint 3.4.1 (101).

## Final arrangement

The actual Fn/Globe modifier is Super. All user-facing Fn bindings are in
`skhd/skhdrc`. No Hyper mapping, Right Option substitution, virtual HID driver,
or alternate window manager is used. The root README lists all active actions.

- macOS symbolic hotkeys 118-122 use ordinary Control+1-5. skhd forwards Fn+1-5.
- WhichSpace uses Control+Shift+1-5 to move and follow a window; skhd forwards
  Fn+Shift+1-5. These are configured recordable bindings, not factory defaults.
- Spotlight retains Command+Space; skhd forwards Fn+Space.
- Vorssaint retains its default Control+Option+Command+V; skhd forwards
  Fn+Control+V. The app's recorder/model does not accept Fn.
- Quit, Lock Screen, and Emoji & Symbols forward to Command+Q,
  Control+Command+Q, and Control+Command+Space respectively.
- App launches use `open`, with the existing mise shims for Herdr and Neovim.
- The compiled Accessibility helper handles Fill/restore, native full screen,
  the Apple menu, and a new Finder window. It inherits the existing caller's
  Accessibility permission and does not require System Events/Apple Events.

Built-in `source | target` forwarding runs inside skhd's event tap. The previous
shell-based forwarding implementation is superseded. Helper actions and app
launch commands still run on demand; there is no always-running helper daemon.

## Verification

These checks used synthetic key events through the running skhd service unless
explicitly described as physical keyboard confirmation.

| Check | Evidence |
|---|---|
| Desktop switching, all five | Active Space IDs matched desktop 1-5: 1, 3, 4, 5, 48. Starting desktop was restored. |
| Move and follow, all five | A temporary Finder window's Space membership and active Space both matched each target; only that test window was closed. |
| Spotlight | One Spotlight window appeared, then was dismissed. |
| Clipboard built-in forwarding | Dynamic Island size changed 333x39 -> 704x403 -> 333x39. No history contents were inspected. User previously confirmed the Fn chord physically. |
| New Finder window | Two presses increased window counts 5 -> 6 -> 7. The two created windows were then closed. |
| Apple menu | Sleep menu item's displayed dimensions were 250x24. Menu dismissed with Escape. |
| Native full screen | After creating and focusing a temporary Finder window, AXFocusedWindow's AXFullScreen changed false -> true -> false, with 1.8 seconds allowed per animation. Helper stderr was empty. Test window closed afterward. |
| Emoji picker | Fn+Control+E in a temporary TextEdit document produced a CharacterPalette window. Picker dismissed and test document closed/deleted. |
| Fill/restore | User confirmed Finder, Chrome, Calendar, and Ghostty. Earlier automated checks passed in Finder and Chrome. |
| App targets | Installed app IDs and paths, including the mise Neovim shim, were checked. Calendar, Mail, and 1Password were not opened solely for inspection. |
| Share / LocalSend | Fn+Control+S invoked the launch command successfully and LocalSend became frontmost. Bundle ID `org.localsend.localsendApp`, installed version 1.18.2. No transfer was started. |
| New terminal window | Fn+Return and its keypad-Enter variant each created one additional Ghostty window. The two new test windows were closed; the existing window was preserved. Uses `open -na /Applications/Ghostty.app` to create a new instance/window on every press. |
| Native Accessibility Zoom | `UAZoomEnabled()` reported false at normal scale, true after Fn+Control+Z, then false after Fn+Control+Option+Z following two zoom-in presses. Repeating reset remained false. Display was left fully zoomed out. |
| LazyDocker | Fn+Shift+D started a new LazyDocker process in Ghostty through the existing mise shim. Installed version 0.25.2; OrbStack's Docker socket was available. No container actions were performed. |
| Activity / btop | Fn+Control+T started a new btop process in a new Ghostty instance. Homebrew executable `/opt/homebrew/bin/btop`, version 1.4.7. |

An earlier full-screen assertion against Finder's front window failed; its exact
cause was not isolated. The final check used AXFocusedWindow after activation
and passed both transitions. Native full-screen animations are asynchronous;
rapid repeated presses during an animation were not tested. No full-screen code
change was required after the focused-window check.

Lock Screen and quit were deliberately not triggered against the user's session.
Their native target chords are configured, but runtime behavior has not been
verified here. Physical confirmation of the remapped Caps Lock plus Fn chord and
the latest new app-launch chords remains separate from the synthetic tests.

No latency improvement is claimed for Fill. Earlier profiling measured roughly
553 ms for an initial Fill versus 117-128 ms for warm presses. The user reported
the behavior was better and moved on. Forwarded chords now avoid a process launch.

## Portability and snapshots

Zoom-in forwards to native Option+Command+= (physical equals keycode 24).
Full reset uses the public `UAZoomEnabled()` API, then invokes the already
authorized skhd binary to post Option+Command+8 only while zoomed in. The installed
macOS SDK's `HIServices.framework/Headers/UniversalAccess.h` explicitly documents
false when Zoom is off or the user is fully zoomed out. No extra helper permission
is required. Enable native keyboard Zoom in System Settings; the portable restore
does not modify Accessibility Zoom preferences.

`macos/desktop-shortcuts.plist` replaces the earlier `fn-desktops.plist` name.
The settings script merges only desktop IDs 118-122 and selected WhichSpace
preferences, preserving unrelated native hotkeys and machine-specific app state.
It compiles the helper only when its source changes or the binary is absent.

Vorssaint backup/restore includes exactly four clipboard configuration keys:
feature availability, history enablement, shortcut enablement, and shortcut.
It never saves the whole Vorssaint domain or clipboard entries. Full native and
WhichSpace rollback snapshots retain machine-specific IDs for this Mac.

The live restore path has been exercised. A fresh-Mac installation, including
privacy approvals and manually creating five desktops, has not been tested.

## Documentation sources

- [skhd.zig](https://github.com/jackielii/skhd.zig): current documentation retrieved
  through Context7 `/jackielii/skhd.zig`, including `|` forwarding syntax.
- [Vorssaint](https://github.com/vorssaint/vorssaint-utils): current documentation
  retrieved through Context7 `/vorssaint/vorssaint-utils`; pinned 3.4.1 source
  inspected for shortcut serialization and default clipboard binding.

Earlier direct-Fn macOS and WhichSpace research files are historical trial
records, superseded by this central routing arrangement.
