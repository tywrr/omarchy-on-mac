# Native searchable keyboard panel

Implemented 2026-10-14 using AppKit and PDFKit. Global Fn bindings remain in
skhd.zig. The app reads its bundled dark PDFs; it registers no global event tap
and requires no Accessibility or Input Monitoring permission.

## Behavior and installation

- Fn+K opens/toggles the macOS sheet; Fn+Control+K opens/toggles Herdr.
- The other hotkey switches the document in the same panel and clears search.
- Search has focus immediately and highlights literal case-insensitive matches.
- Return/Command+G advances; Shift+Return/Command+Shift+G goes back.
- Command+F selects the search field. Escape or Command+W dismisses the panel.
- Escape restores the previous app's focus. Changing apps dismisses the panel.
- The accessory app has no Dock icon and stays idle while hidden. Its floating
  panel joins the current native desktop; it does not create a fullscreen Space.

`scripts/install_panel.py` builds `~/Applications/Omarchy Keys.app` with the local
Swift compiler, bundles both PDFs, and ad-hoc signs the app. Source, metadata,
PDF bytes, and CPU architecture form its build fingerprint. An unchanged install
is skipped; an update restarts only this helper. Portable settings restore calls
the installer before changing the hotkeys. Backups preserve source and resources,
not a machine-specific executable or search history.

The skhd commands use foreground `open -a` URL delivery. Background `open -g`
did not reliably present a cold-launched panel and was removed. Initial URL
events can precede `applicationDidFinishLaunching`, so focus is requested on the
next main-loop turn. Reopen events do not select a document or toggle it again.
Workspace activation notifications preserve the previous app for focus return.

## Verification

The following passed with the installed app and synthetic skhd key events:

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

Final snapshot: `backups/2026-10-15T015253Z/`.

## Primary documentation

- [AppKit application delegate URL delivery](https://developer.apple.com/documentation/appkit/nsapplicationdelegate)
- [NSPanel](https://developer.apple.com/documentation/appkit/nspanel)
- [PDFView.document](https://developer.apple.com/documentation/pdfkit/pdfview/document)
- [PDFDocument.findString](https://developer.apple.com/documentation/pdfkit/pdfdocument/findstring(_:withoptions:))

Current AppKit documentation was fetched through Context7. Installed SDK headers
and compilation verified the concrete AppKit/PDFKit APIs used here.
