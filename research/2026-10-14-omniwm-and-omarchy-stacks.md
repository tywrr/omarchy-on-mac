# OmniWM and dedicated Omarchy-on-macOS projects

Research date: **2026-10-14**. Read-only investigation: downloaded first-party source archives and read local configuration; did not install, launch, run installers, change settings, or grant permissions. Corporate app-policy approval is not established by technical installability.

## Recommendation for this particular setup

Keep **Vorssaint as the app hotkey layer** if it already feels right. It addresses the user's foundation without requiring a desktop environment migration. Add a native-Space mover/snapping layer as needed. **OmniWM is worth evaluating only if automatic tiling, scrolling columns, scratchpads and a Linux-like workspace model are now desired.** It is not simply a lighter hotkey version of BetterTouchTool.

Of the dedicated Omarchy projects, **Macoma, formerly Macarchy, is the most interesting new modular fit for someone keeping native desktops and existing tools**: its October 11 release offers palettes, separate Ghostty profiles and screensavers without installing a shell environment; its optional tiler follows native Spaces, but is experimental and single-display. **omacosy and Omacchiato** pursue a much more complete desktop takeover: bar, WM, remapper, gestures, themes and terminal/shell setup. They are useful design references, but their default installation conflicts with the user's preference to retain native Mission Control gestures and the existing hotkey system.

## Exact evidence snapshots

| Project | Reviewed snapshot | Current status established here |
|---|---|---|
| **OmniWM** | Stable **v0.7.6**, commit `3c0783954604eaa9110d0bdb61fa29f953e738ee` | Release **2026-10-08**; same version already installed locally, build 88. Canary builds also exist; claims below use stable source. [Release](https://github.com/OmniNull/OmniWM/releases/tag/v0.7.6) |
| **omacosy** | Development `main` captured at **`3d9fc08d35b8041c1b32c7a61115b34a84d41669`** | Repository created **2026-08-11**, pre-1.0. Current main includes choices/switching between AeroSpace and OmniWM; this is development source, not a demonstrated stable release package. [Pinned README](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/README.md) |
| **Omacchiato** | Tagged **v2026.09.30.1**, commit `40ef404f5593d4eaf9f738c278747b40b434886f` | Repository created **2026-09-09**; release **2026-09-30**, fork of omacosy around OmniWM. [Release](https://github.com/wicksipedia/omacchiato/releases/tag/v2026.09.30.1) |
| **Macoma / former Macarchy** | Tagged **v0.3.4**; also inspected current main source archive `fa79c3d04665e7a3f6301a05fe1f36c0b859fce7` | Release **2026-10-11**. Capability and installer claims below were checked against the release tag, not only the current README. [Release](https://github.com/theboringhumane/macoma/releases/tag/v0.3.4) |

## Where OmniWM fits

### It manages windows and workspaces, while Vorssaint can continue launching apps

Stable OmniWM offers **two workspace layout engines**:

- **Niri:** scrolling containers/columns, with stacking/tabbed groups.
- **Dwindle:** Hyprland-style binary splits; each new window splits a tile, closer to Omarchy's familiar layout.

They can be selected **per workspace** and switched at runtime. Individual windows/apps may float above either layout via a floating toggle or app rules. The reviewed workspace-layout enum has only `niri` and `dwindle`; there is **no third manual-only/floating-only workspace engine** in this release. Floating some windows does not turn OmniWM into a simple on-demand snap tool. [Stable layout guide](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/guides/layouts.md), [layout enum](https://github.com/OmniNull/OmniWM/blob/v0.7.6/Sources/OmniWM/Core/Config/WorkspaceConfig.swift), [app rules](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/features/app-rules.md).

OmniWM's **command palette launches apps**, searches windows, app menus, files, clipboard entries and its own actions. Its quake terminal is a real **embedded libghostty terminal**, with tabs/splits, rather than an external Ghostty window wrapper. These are genuinely useful extras, but the palette is a search-and-launch interface, not a user-defined shortcut for each app. The stable global command enum does not provide a general arbitrary app-launch or shell-execution action. Both Omarchy stacks therefore put terminal/app/theme/lock hotkeys in Karabiner. **Vorssaint can fill that same conceptual role without adopting their Karabiner layer**, subject to avoiding overlapping chords; coexistence has not been exercised on this machine. [Palette](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/features/command-palette.md), [quake terminal](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/features/quake-terminal.md), [command enum](https://github.com/OmniNull/OmniWM/blob/v0.7.6/Sources/OmniWM/Core/Input/HotkeyCommand.swift), [Omacchiato launch rules](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/bin/omacchiato-karabiner-omniwm).

### Its numbered workspaces are not Apple's numbered desktops

The stable compatibility guide recommends **one native macOS Space per display**, then navigating **OmniWM workspaces**. Its workspace-switch and window-move actions target its own workspace model. This is the important tradeoff: the fast Linux-like layout/workspace experience becomes the primary organizer.

**Native Spaces still exist and extra Spaces are tolerated.** More precisely, inactive native-Space windows remain under macOS control and are not tiled **until that Space is active**. This is more nuanced than saying OmniWM cannot work with native Spaces at all. Native fullscreen also remains available and creates a native fullscreen Space outside the tiled layout. OmniWM's separate fullscreen action expands a window inside its own workspace instead. [Stable compatibility guide](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/help/known-limitations.md#spaces-configuration), [fullscreen distinction](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/guides/layouts.md#fullscreen), [workspace hotkeys](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/guides/keyboard-shortcuts.md).

The sensible test is whether one set of OmniWM workspaces makes native Desktop 1–4 unnecessary. If preserving those numbered Apple desktops is important, native-Space helpers fit better than mapping the same numbers to a second workspace system.

### Ordinary app installation, with meaningful permissions

Official OmniWM releases are **Developer ID signed and Apple notarized**. Stable v0.7.6 supports **Apple Silicon/macOS 26+**, requires **Accessibility + Input Monitoring**, and requires **Displays have separate Spaces**. **Screen Recording is optional** for overview/capture previews; Full Disk Access is optional for Hidden Bar. Normal tiling does not require either optional permission. **SIP stays enabled**; no Karabiner driver or Dock injection is required to use standalone OmniWM. It does use selected private Apple APIs, so future OS updates remain a compatibility concern. [Stable requirements](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/help/known-limitations.md), [installation](https://github.com/OmniNull/OmniWM/blob/v0.7.6/README.md#installation).

OmniWM intentionally refuses to start management beside another resident WM such as AeroSpace, Amethyst, Glide, Paneru, Rift, Nehir or yabai. A hotkey launcher is a different role; Vorssaint is not in its documented conflict list, but that is not a coexistence test. For combined use, let **one app own each physical shortcut** and one WM own frame changes. [Conflict policy](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/help/known-limitations.md#conflicts).

### The local installation already has customized settings

Read from `/Users/tbriles001/.config/omniwm/settings.toml`, without edits:

- Global Hyper chord: **Control + Command**, triggered by **Right Command**.
- Default layout: **Dwindle**; workspaces **1–2 Dwindle**, **3–9 Niri**.
- Workspace 6–7 assigned to secondary monitor; others to main.
- **Hyper + L** toggles workspace layout; **Hyper + W** closes the focused window.
- **Control + Option + Space** opens its palette; **Option + grave** toggles quake terminal.
- Floating toggle unassigned; workspace swipe handling disabled; IPC enabled.

These are saved configuration facts, not proof OmniWM is currently running. A complete stack installer should not be used merely to explore OmniWM: this configuration is already tailored, and a separate hotkey app may compete with its Right Command trigger. Stable OmniWM docs allow **System Hyper Trigger = None** when another tool produces the modifier chord; a future configuration change would need to choose that ownership deliberately. [Stable Hyper instructions](https://github.com/OmniNull/OmniWM/blob/v0.7.6/website/src/content/docs/guides/keyboard-shortcuts.md#customization-and-the-hyper-modifier).

## omacosy and Omacchiato: what their source really does

### Shared goal and architecture

Both recreate more of Omarchy than a few shortcuts: a themed custom status bar, workspace switching, overview, focus borders, gestures, terminal spawning and shell environment. **Super = held Caps Lock emitting Command+Control+Option; tapping Caps Lock sends Escape.** App-launch and script chords are generated as Karabiner rules. They do not preserve the user's Fn convention automatically. [omacosy remap](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/config/karabiner/karabiner.json), [Omacchiato remap](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/config/karabiner/karabiner.json).

| Aspect | omacosy development snapshot | Omacchiato tagged release |
|---|---|---|
| WM | **AeroSpace default**, OmniWM option; manager-switch helpers | **OmniWM only**, minimum version 0.7.0 checked |
| Default OmniWM layout/template | Dwindle; 18 named workspaces split main/secondary in reviewed template | Niri; 9 workspaces, 1–5 main, 6–9 secondary |
| App choices | Config-driven terminal, browser/mail defaults or overrides, Spotify/Slack defaults | Terminal/Ghostty, Safari, Spotify/Slack defaults; generator also hardcodes Outlook/Teams and personal YouTube app path |
| Compiled helper roles | System helper, bar, overview, gesture, WM IPC client, separate focus-follows-mouse and border components for AeroSpace | Five main helper roles: system helper, bar, overview, gesture, WM IPC client; OmniWM supplies tiling/focus borders |
| Delivery | Builds helpers locally; code signing depends on available Apple Development identity | At exact release tag, downloads checksum-verified **team-signed helper bundle**; falls back to build if unavailable/invalid; development `--edge` path builds |
| Update style | Development checkout update/re-run; rejects problematic local edits | Date-tag release update/re-run or explicit development edge path |
| Maturity | Author describes pre-1.0 and testing on one desk, no support promises | Newer fork; author describes narrow desk testing and no support promises |

Sources: [omacosy Brewfile](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/Brewfile), [its installer](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/install.sh), [its OmniWM template](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/config/omniwm/settings.toml), [its launch rules](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/bin/omacosy-karabiner-omniwm), [Omacchiato installer](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/install.sh), [template](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/config/omniwm/settings.toml), [launch rules](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/bin/omacchiato-karabiner-omniwm), [requirements](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/config/requirements.conf), [update implementation](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/bin/omacchiato-update).

### Package and configuration footprint

Both Brewfiles install **Karabiner-Elements, Ghostty, Raycast**, their WM, **fzf, eza, zoxide, ripgrep, bat, lazygit, btop, starship, jq**, and a Nerd Font. Omacchiato additionally installs **gh**. omacosy supports optional yazi installation. They install Homebrew if absent. This is a sizable environment installer even when many dependencies are already present. [omacosy packages](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/Brewfile), [Omacchiato packages](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/Brewfile).

Their installers back up existing non-symlink configuration paths, record displaced symlinks, and then link/copy their own configuration. This includes **Starship and Ghostty**, and substantial **zsh startup changes**. The current omacosy code has explicit zsh-stub/local-config preservation logic; Omacchiato's tagged installer links its own zshrc. Both **copy a complete Karabiner configuration**, preserving a pre-stack backup, then append generated rules. The existing keyboard setup is replaced during normal installation, rather than safely adding just one app chord. [omacosy backup/link handling and zsh logic](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/install.sh#L154), [Omacchiato configuration handling](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/install.sh#L103).

An important difference: omacosy links its OmniWM config directory; **Omacchiato copies its OmniWM settings template only if the settings file does not already exist**. That protects the current layout/key settings from a direct template overwrite, but its theme script subsequently edits OmniWM appearance/border configuration. Theme helpers also set wallpaper and update their own terminal/theme state; Omacchiato integrates Herdr config. **Running only `theme-set` is therefore still a mutation of several existing files**, not just previewing a color palette. [Omacchiato template handling](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/install.sh#L173), [theme implementation](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/bin/theme-set), [omacosy theme implementation](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/bin/theme-set).

They install per-user **LaunchAgents** for custom bar/gesture/focus helpers and start services. Omacchiato also downloads **tokscale** for AI-usage reporting, a glyph-name catalog, and an **AirPods control helper**, with pinned-version/checksum machinery in the installer. Those extras are not needed to satisfy the current app-launch/window-management request. [Installer](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/install.sh).

### Native gestures and appearance are deliberately changed

Both macOS-defaults scripts **auto-hide the native menu bar** and **disable native four-finger vertical/horizontal gestures and Mission Control gesture handling**, handing these inputs to their custom overview/workspace system. Omacchiato also disables **three-finger native fullscreen-Space switching**, to reserve input for its column scrolling. That is a concrete conflict with retaining the ordinary Mission Control gesture experience. Their manifests record original values for uninstall restoration, but default installation still makes these changes. [omacosy defaults](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/macos-defaults.sh), [Omacchiato defaults](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/macos-defaults.sh).

### Privileges, extensions and signing

- **Karabiner requires its privileged service/virtual keyboard driver and user approval of the driver extension**, plus Input Monitoring. The stacks' own helpers generally run as the login user, but their dependency footprint is broader than standalone OmniWM or a hotkey app.
- Window/gesture/bar helpers need **Accessibility**; raw gesture/remap paths use **Input Monitoring**. Captured overview thumbnails need **Screen Recording**, potentially granted to the launching process depending on macOS's permission attribution.
- Helpers use private **SkyLight, MultitouchSupport and DisplayServices** frameworks. No SIP-disable requirement was found in the reviewed stack installers.
- Omacchiato verifies the downloaded release helpers' signing team and checksum. Its installer explicitly comments that **curl does not set quarantine and Gatekeeper therefore does not ask for notarization**. Team-signed helper files are **not equivalent to an Apple-notarized release**; don't transfer standalone OmniWM's notarization claim to the whole stack.
- **Omacchiato's installer also invokes a lid-closed keep-awake setup** that, when run interactively and absent, requests an admin password and writes `/etc/sudoers.d/omacchiato-keep-awake`. The rule allows only two root `pmset disablesleep` forms without a password. Failure leaves that feature unavailable. Thus “our helpers do not run as root” does not mean there are no privileged installation actions. Its removal also needs privileged action.

Sources: [Omacchiato release-fetch code](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/install.sh#L228), [lid setup invocation](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/install.sh#L656), [exact sudoers helper](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/bin/omacchiato-lid-rule), [omacosy permissions](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/README.md#permissions), [Omacchiato permissions](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/README.md#permissions).

### Backups and uninstall are real, but not a zero-risk sandbox

Both projects have manifest-driven uninstall scripts intended to restore preferences/configuration and remove helpers/packages that they introduced while preserving pre-existing packages. Reviewed comments can be stale: Omacchiato's uninstall header says packages are left installed, while its implementation actually removes manifest-recorded added packages. Similarly the launch-rule script comments say OmniWM lacks close-window commands even though stable 0.7.6 already has one. Treat the **implementation and version pairing** as authoritative, not every comment. Backup handling improves reversibility but does not guarantee that later user changes, permission entries, package upgrades or every helper side effect will unwind perfectly. [Omacchiato uninstall](https://github.com/wicksipedia/omacchiato/blob/v2026.09.30.1/uninstall.sh), [omacosy uninstall](https://github.com/paulsp94/omacosy/blob/3d9fc08d35b8041c1b32c7a61115b34a84d41669/uninstall.sh).

## Macoma: a much more modular Omarchy-on-Mac project

**Macoma was previously named Macarchy**, and retains some `macarchy` data paths/bundle identifiers for compatibility. Its latest verified release here is **v0.3.4, October 11, 2026**. It offers:

- **Appearance:** 23 Omarchy palettes, catalog metadata for 96 wallpaper entries, apply/restore and imported images.
- **Terminal:** separate managed Ghostty profiles; optional three-pane tmux Work session using a dedicated socket/server. Normal Ghostty config, shell dotfiles and unrelated tmux servers are preserved.
- **Windows:** optional scrolling columns, stacks, gaps, focus border and keyboard rearrangement, using public APIs on the currently active native Space.
- **Screensavers:** 40 effects, custom text/image artwork and a real system screensaver.

Its app does **not** activate tiling merely on launch, install missing shell tools, or replace shell dotfiles. Each module has explicit controls. **Vorssaint can remain the general app hotkey system while Macoma is used only for appearance, terminal profiles or screensavers**, leaving its window manager disabled. [Release-tag README](https://github.com/theboringhumane/macoma/blob/v0.3.4/README.md).

The optional Windows module requires **Accessibility**, follows **native Space changes** through `NSWorkspace.activeSpaceDidChangeNotification`, and rebuilds its managed active-Space window view. It does **not** implement native Space switching/moving itself. There is **one-display support only**, no trackpad scrolling, no crash recovery and no compositor effects. Pause/quit attempts to restore saved original frames; those originals exist only during the app session. Sleep and display changes pause management. App minimum-size/offscreen clamping remains a documented limitation. Do not run it beside OmniWM as a second frame-controlling WM. [Stable Windows behavior](https://github.com/theboringhumane/macoma/blob/v0.3.4/README.md#scrolling-windows), [stable service implementation](https://github.com/theboringhumane/macoma/blob/v0.3.4/Sources/Modules/Windows/WindowManagementService.swift#L120).

The tagged setup script installs **only to the current user's `~/Applications` and `~/Library/Screen Savers`**, verifies checksums and bundle signatures, checks existing bundle identity, and preserves prior Macoma bundles in a backup directory. It does **not use sudo**, modify lock policy, or install a system-level driver. It requires **Apple Silicon/macOS 15+**. Distribution is **ad-hoc signed, not notarized** unless trusted signing credentials are supplied; Gatekeeper may block downloaded builds. Thus it has a smaller setup footprint than the full stacks, but lower distribution trust/maturity than official standalone OmniWM. [Stable setup script](https://github.com/theboringhumane/macoma/blob/v0.3.4/setup.sh), [installer](https://github.com/theboringhumane/macoma/blob/v0.3.4/scripts/install.py), [qualification report](https://github.com/theboringhumane/macoma/blob/v0.3.4/docs/build-qualification.md).

The developer publishes extensive pure model/identity assertions and a small amount of actual user qualification. Those are useful transparency, **not proof of broad live-app/multiple-monitor compatibility**. The validation note contains a stale Space-change pause checklist, while the tagged service implements active-Space rebuild; actual source and current README agree that it follows Spaces. [Windows qualification](https://github.com/theboringhumane/macoma/blob/v0.3.4/Tests/Windows/VALIDATION.md), [implemented Space change](https://github.com/theboringhumane/macoma/blob/v0.3.4/Sources/Modules/Windows/WindowManagementService.swift#L146).

## What can be borrowed while keeping Vorssaint

| Piece | Useful independently? | What to watch |
|---|---|---|
| App launch chord map from omacosy/Omacchiato | **Yes, as a design reference** | Recreate desired chords in Vorssaint; their generated Karabiner rules depend on helper paths and bundle-specific assumptions. Do not import the complete remapper just for app launch. |
| Standalone OmniWM | **Yes, if willing to use a real tiler/workspace layer** | Retain existing tailored config, resolve Right Command/hotkey ownership, choose optional permissions deliberately. Avoid another resident WM. |
| Palettes, font choices, static terminal theme assets | **Yes** | Extract selected settings; their full theme scripts also rewrite wallpaper, OmniWM and other configs. |
| Stack custom bar/overview/gesture daemons | **Not as simple native-Space drop-ins** | Depend on AeroSpace/OmniWM IPC/workspace models; custom gesture defaults replace Mission Control behavior and require several permissions. |
| Macoma appearance/terminal/screensaver modules | **Yes, explicitly modular** | Ad-hoc distribution; wallpaper behavior over multiple Spaces not fully qualified; optional tiler remains experimental. |
| Full omacosy/Omacchiato installation | **Poor fit for keeping the current input/Desktop setup unchanged** | Karabiner+driver, config replacement, native gesture changes, services, broad dependencies; fork has optional sudoers modification. |

## Other dedicated Omarchy-on-Mac discoveries

These do not replace the native Mac app/window workflow, but explain why newer videos might look like “Omarchy on a Mac.”

- **[Try Omarchy](https://github.com/omacom/try-omarchy)** — latest verified **v0.5.1, October 7, 2026**. Runs an ARM64 **Arch Linux/Omarchy guest** in a QEMU runtime using Apple's Hypervisor framework and a Swift launcher. Signed/notarized app, hardware-accelerated guest graphics. It offers an actual Linux desktop inside an app, rather than putting Finder/Chrome/macOS windows under Omarchy's WM. [Release](https://github.com/omacom/try-omarchy/releases/tag/v0.5.1).
- **[OmacVM](https://github.com/gillesgoetsch/omacvm)** — **v3.1.9, October 14, 2026**, discovered during this research. Full Omarchy VM setup with Mac hardware/input integration. **[Omanotch](https://github.com/gillesgoetsch/omanotch)** is now part of OmacVM, placing the guest's real bar into the MacBook notch area. This is a VM experience; installer/permissions were not deeply audited here. [Release](https://github.com/gillesgoetsch/omacvm/releases/tag/v3.1.9).
- **[iOmarchy](https://github.com/jamesyork-prog/iomarchy)** — explicitly independent personal fork of Try Omarchy, with separate app/VM identity. Another Linux guest experience, not a native Mission Control enhancement.
- **[Omacy](https://github.com/dedene/omacy)** — **v0.1.5, September 3, 2026**, focused macOS Omarchy ASCII screensaver, signed/notarized by Zenjoy BV, macOS15+/AppleSilicon. Potentially useful without a WM/remapper migration. [Release](https://github.com/dedene/omacy/releases/tag/v0.1.5).
- **[Cinder Bar](https://github.com/simoz/cinderbar)** — native port of the Omarchy Burn Bar plugin for local Claude/Codex usage budgets. An appearance/usage accessory, not app hotkeys or window management.

All these are first-party projects; their claims of hardware/performance/privacy were not independently benchmarked. No date beyond October 14, 2026 was treated as a shipped release. This is a targeted catalog, not a claim that all possible projects have been found.

## Practical decision

**Keep-native path:** Vorssaint for app hotkeys, actual Mission Control desktops, native window controls or a focused snap/move helper. Borrow Omarchy themes selectively, or inspect Macoma's modular appearance/terminal/saver features.

**Middle path:** Vorssaint plus standalone already-installed OmniWM. Test Dwindle for familiar Omarchy splitting and Niri for wide-monitor scrolling. Expect its own workspace layer to become the main organizer. Don't run a full desktop installer just to access OmniWM.

**Full environment path:** omacosy/Omacchiato if the bar, custom gestures, CapsLock Super, themed shell/terminal and managed workspaces are part of the desired outcome. Their sources make the setup concrete and largely reversible, but they are a much larger workflow and corporate-installation decision.
