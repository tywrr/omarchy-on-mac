# Native searchable keyboard panel

Implemented 2026-10-14 using AppKit and PDFKit. Global Fn bindings remain in
skhd.zig. The app reads its bundled dark PDFs; it registers no global event tap
and requires no Accessibility or Input Monitoring permission.

## Behavior and installation

- Fn+K opens/toggles the macOS sheet; Fn+Control+K opens/toggles Herdr.
- The other hotkey switches the document in the same panel and clears search.
- Search has focus immediately and highlights literal case-insensitive matches.
- Return/Command+G advances; Shift+Return/Command+Shift+G goes back.
- Command+F selects the search field. Escape or Command+W closes and quits the app.
- Escape restores the previous app's focus. Changing apps closes and quits the app
  without taking focus away from the newly selected app.
- The accessory app has no Dock icon and runs only while in use. Its floating
  panel joins the current native desktop; it does not create a fullscreen Space.

`scripts/install_panel.py` builds `~/Applications/Omarchy Keys.app` with the local
Swift compiler, bundles both PDFs, and ad-hoc signs the app. Source, metadata,
PDF bytes, and CPU architecture form its build fingerprint. An unchanged install
is skipped; an update stops only this helper. The next hotkey launches it again.
Portable settings restore calls
the installer before changing the hotkeys. Backups preserve source and resources,
not a machine-specific executable or search history.

The skhd commands use foreground `open -a` URL delivery. Background `open -g`
did not reliably present a cold-launched panel and was removed. Initial URL
events can precede `applicationDidFinishLaunching`, so focus is requested on the
next main-loop turn. Reopen events do not select a document or toggle it again.
Workspace activation notifications preserve the previous app for focus return.

## Verification

The following passed with the initial resident version and synthetic skhd key events:

| Check | Result |
|---|---|
| Cold Fn+K | Panel onscreen, correct document, search focused |
| Type `finder` using ordinary key events | Full query entered; 2 matches |
| Return then Shift+Return | 2/2 then 1/2 |
| Fn+Control+K while macOS sheet is open | Herdr sheet; empty search |
| Type `workspace` | Full query entered; 7 matches |
| Command+F then a missing word | Search selected; `No matches` feedback |
| Escape while search has focus | Panel hidden; previous app restored |
| Warm reopen | Search cleared |
| Repeat the same hotkey | Panel hidden; previous app restored |
| Command+Tab away from the panel | Panel dismissed |
| Portable restore dry run | No differences in panel, skhd, or preferences |

The panel screenshot and both updated macOS PDF renderings were visually
inspected. `skhd --text Finder` inserted only `Fi` in an early automation test;
the definitive typing checks used individual normal key events and passed.
The user also confirmed both physical hotkeys, searches, and Escape dismissal
work. Native fullscreen/multiple-monitor presentation has not been separately
exercised.

Initial panel snapshot: `backups/2026-10-15T015253Z/`.

## On-demand lifecycle

The default now quits the app when dismissed, at the user's request to prioritize
RAM over reopening speed. Escape, Command+W, the close button, repeating the same
hotkey, and switching to another app all terminate the process. Explicit dismissal
returns focus to the previous app. Switching away preserves the newly selected
app's focus. Switching sheets keeps the current panel process and clears search.
There is no background panel process or retained in-process document cache after
dismissal. The existing skhd commands cold-launch the app on the next press.

Before this change, the resident app used about 76 MB and sampled at 0.0% CPU when
idle, both hidden and showing the sheet. Five paired tests measured a median
114 ms to reopen the hidden panel (range 106–206 ms), compared with 545 ms after
quitting the process (range 505–615 ms). The initial reopen after a longer idle
was 159 ms. These timings include `open -a` URL delivery and end when the panel
is onscreen and frontmost; they do not measure completed PDF rasterization or
a first launch after reboot. They describe the earlier resident build, not a
new benchmark of the on-demand build.

The updated installed app passed these integration checks using real skhd key
events and native Accessibility inspection with existing permissions:

| Check | Result |
|---|---|
| Cold Fn+K, search `finder` | macOS sheet; 1 / 2 matches |
| Fn+Control+K, search `workspace` | Herdr sheet; 1 / 7 matches; same process |
| Escape | Process exits; previous app regains focus |
| Next Fn+Control+K | New process launches the Herdr sheet |
| Repeat Fn+Control+K | Process exits; previous app regains focus |
| Command+W | Process exits; previous app regains focus |
| Close button | Process exits; previous app regains focus |
| Switch to another app | Process exits; selected app keeps focus |
| Portable restore dry run | No panel, skhd, WhichSpace, or native settings differences |

Final live state has no `OmarchyKeys` process. Updated snapshot:
`backups/2026-10-15T022101Z/`. No PDF, global shortcut, or application permission
changed for this lifecycle update.

## Primary documentation

- [AppKit application delegate URL delivery](https://developer.apple.com/documentation/appkit/nsapplicationdelegate)
- [NSPanel](https://developer.apple.com/documentation/appkit/nspanel)
- [PDFView.document](https://developer.apple.com/documentation/pdfkit/pdfview/document)
- [PDFDocument.findString](https://developer.apple.com/documentation/pdfkit/pdfdocument/findstring(_:withoptions:))

Current AppKit documentation was fetched through Context7. Installed SDK headers
and compilation verified the concrete AppKit/PDFKit APIs used here.
