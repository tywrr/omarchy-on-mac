# Fn app-launch hotkeys in skhd.zig

Configured 2026-10-14 after the user installed and started skhd.zig
`0.2.0-7e95d99 (fast)`.

The working config is now tracked at [skhd/skhdrc](../skhd/skhdrc), with
[full live backups](../backups/) and portable native/WhichSpace restore settings.

## Active configuration

The live config is `~/.config/skhd/skhdrc`. It was empty before
this change. Its backup is
`~/.config/skhd/skhdrc.before-app-launches-20261014-120254`.

Super means the actual Fn/Globe modifier; no key remapping is involved.

| Binding | Action |
|---|---|
| Fn + Control + Q | Open/focus Calculator |
| Fn + Return | Open/focus Ghostty |
| Fn + Control + Return | Start Herdr in a new Ghostty instance |
| Fn + Shift + Return | Open/focus Google Chrome |
| Fn + Shift + Option + B | Open a new Chrome incognito window |
| Fn + Shift + F | Open/focus Finder |

App launches use `/usr/bin/open` and installed bundle identifiers. Herdr retains
the existing BTT command:

```sh
/usr/bin/open -na /Applications/Ghostty.app --args -e "$HOME/.local/share/mise/shims/herdr"
```

Chrome incognito uses `open -na` with `--incognito --new-window` so arguments
are delivered even while Chrome is running. Each press requests a new window.

Return bindings cover both the regular Return virtual key and `0x4c` (keypad
Enter), since the existing BTT preset records Apple Fn+Return as keypad Enter.

## Verification

The running service accepted `skhd --reload`; no new errors were added to its
log. Its event tap was active before and after configuration. BTT was not running.

Simulated hotkeys using the installed `skhd --key` exercised the running handler:

- Calculator, Ghostty, Chrome, and Finder became frontmost as expected.
- Both regular Return and keypad Enter variants focused Ghostty and Chrome.
- Fn+Shift+Option+B increased Chrome's window count from one to two; the new
  window title explicitly identified it as Incognito.
- Fn+Control+keypad Enter launched a new Ghostty process with the expected
  `-e` command and a new Herdr process. No Herdr pane/session control commands
  were used.
- A subsequent plain Fn+keypad Enter focused the original Ghostty instance,
  rather than the separate Herdr instance.

These are synthetic-event tests. Physical keyboard confirmation was requested
and is pending as of this report.

Read-only preference exports confirmed native desktop-switch IDs 118–122 still
use Fn+1–5, and WhichSpace's five move bindings still use Fn+Shift+1–5. The skhd
config does not register those chords.

Only ordinary hotkeys are configured. The service reports no skhd-grabber/HID
daemon installed; no remapping directives or driver installation were added.

## Maintenance

Edit the live config and run `skhd --reload` if needed. The service also supports
automatic config reloads. To undo this change, restore the backup above and
reload skhd. Preserve later edits if restoring after adding more bindings.

Syntax and reload reference: <https://github.com/jackielii/skhd.zig/blob/main/SYNTAX.md>
and <https://github.com/jackielii/skhd.zig/blob/main/README.md>.
