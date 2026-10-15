# Searchable shortcut windows for macOS and Herdr

Researched 2026-10-14. No apps installed and no runtime shortcut settings changed.

The desired behavior is two distinct windows: **Fn+K** for the macOS/skhd bindings and **Fn+Control+K** for Herdr. Each should support text search, dark appearance, and Escape dismissal. The existing PDFs contain searchable text; an image is unnecessary for search.

## Recommendation

A small native AppKit/PDFKit panel is the closest fit for the exact two-document behavior. It can reuse the existing dark PDFs, expose search, hide immediately on Escape, and restore the previously active application. skhd can handle the global Fn bindings, so the viewer itself need not register global keys or request Accessibility permission. This is a proposed implementation, not a completed app.

**KeyClu is the closest existing application.** It now supports skhd hotkeys and manually imported custom shortcuts, rather than only showing app menus. Its search, dark appearance, panel controls, and CLI make it worth testing if an extra Accessibility permission is acceptable. Exact two-sheet routing and the installed skhd.zig grammar remain unverified.

## Existing applications

| Option | Verified strengths | Limits for this setup |
| --- | --- | --- |
| [KeyClu](https://sergii.tatarenkov.name/apps/keyclu) | Current release 0.32, July 2026. Search/highlight, light/dark/system appearance, persistent panel, custom shortcuts, skhdrc reader, and CLI panel controls. Distributed free with BSD-3-Clause-Clear license. | Requires Accessibility to detect the active application. Documentation does not establish Escape dismissal, parsing of skhd.zig `|` key forwarding, or selection of an arbitrary custom Herdr collection through CLI. |
| [KeyCue](https://ergonis.com/en/keycue) | Commercial native overlay showing application and system shortcuts; text search; configurable activation; hands-free mode keeps the window open. | More focused on application/menu/system shortcut discovery. The sources reviewed do not establish automatic skhdrc import, two arbitrary named cheat sheets selected by CLI, or the required Escape behavior. |
| [KeyCombiner Desktop](https://keycombiner.com/desktop/) | Global instant lookup includes personal collections plus active-application shortcuts; searchable custom shortcut/text collections. Two collections available with a free account. | Account and collection workflow is larger than a simple local viewer. CSV import and dark mode are Pro features. Accessibility needed for active-app detection; browser-aware lookup additionally needs Automation. No documented independent hotkeys to two selected collections or Escape dismissal in reviewed sources. |

### KeyClu integration details

[Official skhd integration documentation](https://github.com/Anze/KeyCluCask/wiki/Integrations-%E2%80%90-skhd) says it reads `$XDG_CONFIG_HOME/skhd/skhdrc`, `$HOME/.config/skhd/skhdrc`, and `$HOME/.skhdrc`. A comment immediately before each shortcut supplies its display description. A comment such as `#KeyClu[Window management]: Fill window` supplies a named group. Supported key forms include `a`, `1`, `kVK_ANSI_A`, and `0x2b`; some named special keys are unsupported. The documentation names conventional skhd, not skhd.zig, so compatibility with our pipe-based event forwarding should be tested rather than assumed.

[Official CLI documentation](https://github.com/Anze/KeyCluCask/wiki/Integrations-%E2%80%90-CLI-params) explicitly permits controlling an already running instance from skhd or BetterTouchTool. Documented arguments include `--show-shortcuts`, `--toggle-persistent`, `--toggle-panel`, `--columns 5`, `--sheet skhd`, and `--mode skhdmode`. Documented sheet identifiers are KeyClu, macOS shortcuts, macOS gestures, Jitouch, and skhd. An arbitrary collection name or application bundle ID is not documented as a CLI selector.

[My Shortcuts](https://github.com/Anze/KeyCluCask/wiki/My-Shortcuts) documents JSON `.keyclu` import/export and global or per-application custom shortcuts. Supported modifier names include `shift`, `control`, `option`, `command`, and **`fn`**. A Herdr collection can therefore be imported as custom content. Since Herdr runs inside Ghostty, app-bundle-based automatic selection would identify Ghostty; it would not inherently distinguish a Herdr terminal from another Ghostty window. Whether Fn+Control+K can select that custom group directly remains unverified.

### Other product evidence

[KeyCue's official getting-started guide](https://help.keycue.ergonis.com/hc/en-us/articles/23090906791452-How-to-start-with-KeyCue) documents typing into its search bar and hands-free mode. It also documents configurable trigger actions and selecting menu, system, or macro hotkey content. It does not establish the required custom two-document workflow.

[KeyCombiner's feature matrix](https://keycombiner.com/features/) documents two collections for a free account, filter/search, and desktop instant lookup. CSV import, dark mode, unlimited collections, and exports are Pro features. Its [desktop page](https://keycombiner.com/desktop/) documents the changeable global instant-lookup shortcut and permission requirements. Its [author's description](https://tkainrad.dev/posts/app-to-show-shortcuts-of-current-application-windows-linux-macos) describes lookup as searchable, including personal collections and text snippets, and working offline after startup synchronization.

## Native and PDF alternatives

| Option | What it provides | What remains missing |
| --- | --- | --- |
| [Quick Look](https://support.apple.com/guide/mac-help/preview-a-file-mh14119/mac) | Minimal native file preview. Apple documents Space or Escape closing the preview. | Full text search is not documented on this help page; do not assume it supports the desired search interaction. |
| [Preview](https://support.apple.com/guide/preview/find-text-in-pdfs-prvw2014/mac) | Existing searchable PDFs work directly; native Find searches PDF text. | More window chrome. Escape is not the standard command for closing its document window. |
| [Skim](https://sourceforge.net/p/skim-app/wiki/Tips_and_Tricks) | Dedicated PDF reading alternative with search and full-screen/presentation modes. | Its documented Escape behavior exits Find, Overview, full-screen, or presentation modes; that does not establish unconditional close-on-Escape. |
| Native PDFKit panel | Exact document selection, search field, Escape dismissal, chosen visual chrome and focus behavior. Uses the already-generated PDFs. | Needs a small custom viewer implementation and verification. |

Apple's [PDFView.document](https://developer.apple.com/documentation/pdfkit/pdfview/document) and [PDFDocument.findString](https://developer.apple.com/documentation/pdfkit/pdfdocument/findstring(_:withoptions:)) document native PDF display and text search. Live checks of the existing dark files found searchable text: macOS `Finder` (2), `desktop` (4), `Chrome` (1), and `Wi-Fi` (1); Herdr `pane` (8), `tab` (9), and `workspace` (7). Four PNG renderings also exist in ignored `tmp/pdfs/`; those are useful previews but do not preserve the PDFs' text search.

## What has not been proven

No application here has been installed or interactively tested in this research pass. In particular, KeyClu Escape behavior, skhd.zig passthrough syntax, per-collection CLI routing, and performance on this corporate Mac remain unverified. The public KeyClu repository provides distribution material and wiki documentation; it does not provide sufficient app source here to resolve those runtime questions.
