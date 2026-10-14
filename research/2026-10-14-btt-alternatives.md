# BetterTouchTool alternatives for the Omarchy-on-Mac workflow

Research snapshot: **14 October 2026**. Three research agents independently investigated app hotkeys, manual/native window controls, and newer desktop/workspace utilities. The catalog covers **53 tool families**, counting the three unrelated Glide projects and two MacTile projects separately, and Rectangle/Rectangle Pro together. This is broad discovery, not a claim to list every application in existence.

## Recommendation

**Updated after the source-level follow-up: keep Vorssaint as the preferred foundation.** Its installed v3.4.1 already ships dedicated app hotkeys, direct executable-script hotkeys and extensive window-placement hotkeys. The first broad pass missed these Command Bar capabilities. Local preferences show those bundled feature modules are currently uninstalled inside Vorssaint; that is different from the product lacking them. The remaining hard gaps are Fn/Globe in its shortcut model and exposed numbered native-Space switch/send actions. See the [Vorssaint deep dive](2026-10-14-vorssaint-deep-dive.md) for pinned source, local verification and exact setup paths.

**Native switching implementation:** [Fn+1–5 now work directly through macOS](2026-10-14-native-fn-desktop-test.md), verified with BTT absent and physical Fn+1/Fn+2 confirmed by the user. No companion is needed for desktop switching. Sending windows to numbered desktops and Fn app-launch bindings remain separate migration work.

**Window transfers now implemented:** [WhichSpace directly handles Fn+Shift+1–5](2026-10-14-whichspace-fn-move-test.md) via saved settings, despite its recorder omitting Fn. The user confirmed physical Fn+Shift+1/Fn+Shift+2 move the focused window and follow it. No BTT/Raycast/script dispatcher is needed for these transfers. References below to requiring a Fn bridge for WhichSpace are superseded by this live verification; Vorssaint's own app-hotkey Fn gap remains.

If supported Command/Control/Option/Shift chords are acceptable, **Vorssaint plus WhichSpace invoked through saved scripts** is the smallest documented design to evaluate for the foundation. If exact Fn layers must remain, the already-installed **Raycast plus WhichSpace** is still a relevant alternative hotkey layer, or existing BTT can temporarily retain only those unsupported bindings. Raycast's current manual explicitly documents Fn+key and Fn+Control+key; WhichSpace's stable release documents numbered Space switches and per-window desktop moves. These integrations have not been tested on this machine. [Raycast Fn hotkeys](https://manual.raycast.com/command-aliases-and-hotkeys), [WhichSpace stable actions](https://github.com/gechr/WhichSpace/blob/v1.4.1/README.md#shortcuts).

The follow-up also examined **standalone OmniWM**, the actual installers for **omacosy/Omacchiato**, and newly discovered **Macoma** (formerly Macarchy). Macoma is a more modular Omarchy-style project; the full stacks make much broader input, shell, terminal and gesture changes. See [OmniWM and dedicated stacks](2026-10-14-omniwm-and-omarchy-stacks.md). Apple's macOS26/27 window/Spaces comparison is in the [native macOS follow-up](2026-10-14-native-macos-26-vs-27.md).

**rcmd standalone v3 is the strongest consolidated alternative found.** It combines app opening/focusing, real numbered Mission Control Spaces, window transfers, and saved layouts. Version 3 introduced Fn trigger support; stable 3.6.4 shipped October 5 and can run zsh/AppleScript items in a Stage. Exact arbitrary Fn+Shift/Control/Option bindings remain unverified. Pro is €15 lifetime; the current switcher requires Screen Recording in addition to its Accessibility/Automation setup. [Product](https://lowtechguys.com/rcmd/), [changelog](https://files.lowtechguys.com/rcmd/changelog.html), [dated update feed](https://files.lowtechguys.com/rcmd/appcast.xml).

**Tuna and Glide by Vatsal057 are the especially interesting newer broad utilities.** Tuna succeeds Leader Key and offers direct hotkeys, nested Combo Mode, scripts and window commands. Glide offers a free BTT-like action system with global hotkeys, app opening, snapping, menus and scripts. Neither was proven to preserve every Fn layer and perform direct numbered native-Space transfers on its own. [Tuna](https://tunaformac.com), [Leader Key successor notice](https://github.com/mikker/LeaderKey), [released Glide action catalog](https://github.com/Vatsal057/Glide/blob/v2.4.0/docs/03-actions.md).

For the literal requirement to use **Apple's own native window tiling**, Apple's built-in Fn+Control shortcuts already cover fill, halves, center, restore and some multi-window arrangements. **WindowKeys** adds customizable shortcuts for Apple's Window-menu tiling. Neither alone is a full app-launch/desktop-send replacement. [Apple macOS26 tiling](https://support.apple.com/guide/mac-help/mchl9674d0b0/26/mac/26), [WindowKeys](https://www.apptorium.com/windowkeys).

## Why the exact requirements matter

The existing BTT preset contains 27 enabled shortcuts and 2 disabled shortcuts. It uses Fn/Globe as Super, with additional Shift, Control and Option layers. It launches Ghostty, Chrome, Zed, Herdr, Finder, Calendar, Mail, Calculator and 1Password; switches desktops 1–4; moves windows to desktops 1–4; and controls adjacent Spaces, Stage Manager and native fill.

These are separate capabilities:

1. **App hotkeys:** launch/focus/toggle an app or run a script globally.
2. **Manual window controls:** set size and position on the current desktop or a monitor.
3. **Native Space control:** switch to a numbered Apple desktop and send one window there.
4. **Exact keyboard grammar:** keep Fn+Shift/Control/Option combinations distinct.

Most snapping utilities cover item 2. A saved layout, app profile, zone arrangement, monitor move, or third-party workspace does not establish item 3. An all-four-modifier Hyper key consumes Shift/Control/Option and therefore changes item 4. Raycast's currently documented Fn support is unusually relevant here.

## Practical shortlist

| Option | Recent evidence | What it would replace | Material limits |
|---|---|---|---|
| **Raycast + WhichSpace** | Raycast 2.8 October14; WhichSpace1.4.1 October13 | App hotkeys/scripts, manual window sizes, numbered Apple Space switch/send/move through automation | Current Fn docs not tested on installed Raycast2.4.1; WhichSpace's own recorder cannot use Fn; integration must use Raycast/Shortcuts/scripts; native movement uses private APIs; downloaded binary notarization unverified |
| **rcmd standalone v3** | 3.6.4 October5; beta3.7 October9 | App switching/launching, numbered native Spaces, per-window transfer, saved launch/layout stages | Additional Fn modifier layers unverified; Pro needed for sends/stages; Screen Recording required for current switcher; different grammar from arbitrary BTT shortcuts |
| **Glide — Vatsal057** | New repository March2026; 2.4.0 September24 | Global app hotkeys, snapping, gestures, menus/scripts/Shortcuts | Fn unverified; no native numbered window-send action; separate helper needed; release signing/notarization not established |
| **Tuna** | Current0.106; September2026 update material | App/command hotkeys, leader sequences, scripts, window actions | Fn and numbered native-Space transfer unproven; nested mode is an optional different workflow; free soft limits or $49 once/3 Macs |
| **WindowKeys** | 3.0.1 June25 2025 | Custom shortcuts that invoke Apple's native tiling | No app launch or native desktop sending advertised; Fn recorder support unverified; free |
| **Moom4** | 4.6 August19 2026; app-launch layouts added May2025 | Keyboard positioning, grids, chains, launch-and-restore window layouts | Native desktop-number sending not documented; direct all-purpose app hotkeys not equivalent to layout launch; $15 |
| **mimi** | New June2026; 0.21.0 October10 | Numbered native desktops/window transfers plus manual sizes/focus, with tiling optional | Explicit beta; private Apple APIs; ad-hoc signed/not notarized; requires external hotkey front end; free/MIT; SIP remains enabled |
| **Loop** | Stable1.4.2 January26; Space-send feature merged July2 2026 | Keyboard/mouse snapping, cycles, custom sizes; promising direct native desktop sending | The new desktop-send feature is in rolling prerelease, not established in latest stable; app launch hotkeys not advertised; free |

WhichSpace supports moving windows on **Sonoma or Tahoe26.4+** and explicitly excludes Sequoia. This Mac's verified **26.7.1** meets that documented requirement. **Send** leaves the user on the current desktop; **Move** follows the window. [Version-pinned compatibility and behavior](https://github.com/gechr/WhichSpace/blob/v1.4.1/README.md#moving-windows).

Raycast's cross-platform manual is a potential trap: its numbered `Move to Desktop1–9` commands are marked **Windows**, while `Move to Previous/Next Space` is macOS. Do not assume Raycast alone covers Fn+Shift+1–4. WhichSpace supplies the numbered native-desktop gap. [Manual with platform badges](https://manual.raycast.com/window-management).

## Complete discovery index

Details, prices and permissions are in the three linked research reports. Dates here are latest verified releases or specifically labeled project milestones; an updated old product is not a newly launched one. Each name links to a first-party source.

### App hotkeys and broad automation: 17

| Tool | Freshness / role |
|---|---|
| [Raycast](https://manual.raycast.com/command-aliases-and-hotkeys) | Established; v2.8 October14 2026; Fn hotkeys, apps, manual window controls; already installed |
| [rcmd](https://lowtechguys.com/rcmd/) | Major v3 expansion; stable3.6.4 October5 2026; native Spaces/app/layout utility |
| [Tuna](https://tunaformac.com) | Newer Leader Key successor, current0.106; launcher/hotkeys/Combo Mode/scripts |
| [Leader Key](https://github.com/mikker/LeaderKey) | 1.17.3 September23 2025; creator now focuses Tuna |
| [SpaceLauncher](https://spacelauncherapp.com) | 3.5.7 October9 2026; app/script/menu actions through configurable leader styles |
| [SnapHotkey](https://www.snaphotkey.com) | 2026 developer posts and current1.1.2; dedicated app hotkeys/toggle/cycle |
| [Vorssaint](https://github.com/vorssaint/vorssaint-utils) | 3.4.1 October8 2026; shipping app/script/window hotkeys and configurable Super output; Fn excluded; native numbered Space actions still requested; already installed |
| [skhd.zig](https://github.com/jackielii/skhd.zig) | 0.2.0 July20 2026; lightweight Fn-aware hotkey daemon, separate window engine required |
| [Hammerspoon](https://www.hammerspoon.org) | 1.1.1 February26 2026; Lua automation/window/Space control; standard hotkey API lacks Fn |
| [Alfred](https://www.alfredapp.com/changelog/) | 5.8.1 September24 2026; workflow hotkeys/scripts; Alfred6 is preview evidence, not a verified released version |
| [Keyboard Maestro](https://www.keyboardmaestro.com/main/) | Established, current11.1.1; comprehensive macros/window/menu/script actions |
| [Keyboard Cowboy](https://github.com/zenangst/KeyboardCowboy) | 3.28.4 December13 2025; free MIT GUI automation/workflows |
| [Keysmith](https://www.keysmith.app) | Mature macro recorder; latest published release notes June2024, not a fresh release |
| [Hyperkey](https://hyperkey.app) | Modifier helper; default all-four Hyper changes the current layered Fn model |
| [Superkey](https://superkey.app) | Modifier helper plus text/OCR navigation; current1.66, release date not verified |
| [Thor Launcher](https://apps.apple.com/us/app/thor-launcher/id1120999687) | 1.5.17 May3 2025; minimal app hotkeys |
| [KeyClu](https://sergii.tatarenkov.name/apps/keyclu) | January2026 version history; cheat-sheet adjunct rather than action execution engine |

### Manual/native window utilities: 13

| Tool | Freshness / role |
|---|---|
| [WindowKeys](https://www.apptorium.com/windowkeys) | 3.0.1 June25 2025; actual Apple Window-menu tiling shortcuts |
| [Loop](https://github.com/mrkai77/Loop) | Stable1.4.2 January26 2026; native desktop sends in rolling prerelease |
| [mimi](https://github.com/y3owk1n/mimi) | First0.1 June1 2026; 0.21 October10; native Spaces/manual control, optional tiling |
| [BentoBox](https://bentoboxapp.com) | 1.0 December2025; 1.1.10 August21 2026; per-Space custom zones |
| [MacsyZones](https://macsyzones.com) | 3.1.1 September15 2026; free custom zones remembered per native Space/display |
| [Moom4](https://manytricks.com/moom/) | 4.6 August19 2026; launch-and-arrange layouts added in2025 |
| [Wins](https://wins.cool) | 3.6 September15 2026; native tiling integration, enhanced Mission Control/Dock/Cmd-Tab |
| [Swift Shift](https://www.swiftshift.app) | 1.5.0 September18 2026; Linux-like modifier+mouse window move/resize |
| [Lasso](https://thelasso.app) | Manual layout/grid/shortcut tool; current release date/price not pinned |
| [Rectangle / Rectangle Pro](https://rectangleapp.com/pro) | Established active snapping/window-layout tools; direct native numbered Space sending not established |
| [Magnet](https://magnet.crowdcafe.com) | Established App Store snapper; official FAQ explicitly excludes arranging across Spaces |
| [Swish](https://highlyopinionated.co/swish) | Gestures and keyboard equivalents for window/screen/Space controls; numbered Space sending not verified |
| [1Piece](https://app1piece.com/download/) | 5.1 October10 2026; broad utility, but author says unnotarized and untested on macOS26+ |

### Native-Space helpers and newer focus/layout utilities: 8

| Tool | Freshness / role |
|---|---|
| [WhichSpace](https://github.com/gechr/WhichSpace) | 1.4.1 October13 2026; native numbered switch/send/move and automation |
| [Space Rabbit](https://github.com/Tahul/space-rabbit) | Project April2026; 2.6.1 October2; native Space acceleration and Fn/Globe cycling |
| [InstantSpaceSwitcher](https://github.com/jurplel/InstantSpaceSwitcher) | Project December2025; 3.1 October5 2026; native Space acceleration; unsigned |
| [strafe](https://github.com/rileycx/strafe) | Project August2026; 0.1.2 September17; experimental native Space swipe/hotkey helper |
| [HopTab](https://github.com/royalbhati/HopTab) | Project February2026; 1.4 June18; app/profile/layout helper tied to native desktops; unnotarized |
| [Reef](https://github.com/gouwsxander/Reef) | Project September2025; 1.1 September26 2026; app/window focus scoped to current Space |
| [Glide — Vatsal057](https://github.com/Vatsal057/Glide) | Project March2026; 2.4 September24; free BTT-like hotkeys/actions/gestures |
| [Glide — drluckyspin](https://glideapp.app) | Project March2026; 1.3.2 June18; narrow move/resize utility, author says signed/notarized |

### Automatic tilers and replacement workspace environments: 15

These are included for discovery completeness. Several are a poorer fit than a manual hotkey utility, and their workspace models differ.

| Tool | Freshness / relationship to native desktops |
|---|---|
| [Glide — glide-wm](https://github.com/glide-wm/glide) | 0.2.16 September28 2026; i3/Sway-like tiling within existing native Spaces |
| [Paneru](https://github.com/karinushka/paneru) | Project March2025; 0.5.2 October2 2026; Niri-like scrolling within native Spaces |
| [Amethyst](https://github.com/ianyh/Amethyst) | Established; 0.24.3 April2 2026; automatic tiling on native Spaces |
| [PaperWM.spoon](https://github.com/mogenson/PaperWM.spoon) | Established2021; Hammerspoon scrolling tiler with native Space switch/move actions |
| [MacTile — Grafikart/MacTile.app](https://github.com/Grafikart/MacTile.app) | Project March2026, no release tags verified; BSP tree per native Space |
| [MacTile — yashas-salankimatt](https://github.com/yashas-salankimatt/MacTile) | Project January2026; 1.5 March11; manual grid overlay rather than a replacement desktop manager; no Developer ID signing |
| [OmniWM](https://github.com/OmniNull/OmniWM) | Project October2025; 0.7.6 October8 2026, installed; Dwindle/Niri and own workspace layer |
| [AeroSpace](https://github.com/nikitabobko/AeroSpace) | 0.21.3-Beta July16 2026; own emulated workspaces, SIP stays enabled |
| [FlashSpace](https://github.com/wojciech-kulik/FlashSpace) | Project January2025; 4.18.79 September7 2026; explicitly replaces native Spaces with hide/show workspaces |
| [Rift](https://github.com/acsandmann/rift) | Project July2025; 0.6.9 October7 2026; virtual groups inside managed native Space |
| [Nehir](https://github.com/apphane-dev/nehir) | Project May2026; 0.6.0-rc.44 August13; Niri-like columns/workspaces, native interaction unproven |
| [WinMux](https://github.com/ZimengXiong/WinMux) | Project March2026; 0.5.6 September19; project/workspace/tab/tiling environment; unnotarized |
| [omacosy](https://github.com/paulsp94/omacosy) | Project August2026; pre1.0 full Omarchy-style stack, broader setup and Karabiner driver |
| [Omacchiato](https://github.com/wicksipedia/omacchiato) | Project September2026; release September30; OmniWM-based full stack and Karabiner driver |
| [yabai](https://github.com/koekeishiya/yabai) | Established; 7.1.25 May8 2026; native Spaces, but advanced scripting-addition features need partial SIP disable/Dock injection |

**Naming collisions:** the three Glide projects above are unrelated. The two MacTile projects are unrelated. The manual-grid MacTile is listed with managers only to keep the similarly named projects adjacent; it does not introduce a replacement workspace system.

## Corporate installation assessment

Read-only local inspection found **Raycast2.4.1, OmniWM0.7.6, Vorssaint3.4.1 and BTT6.885 already installed**. This proves installation, not permission grants or employer approval for every feature. No app was installed, updated, configured or trialed during research.

The lowest-disruption path keeps preferred Vorssaint, enables its bundled app/script/window modules, and retains BTT only for unsupported Fn/native-desktop bindings until a replacement is verified. If different modifier chords are acceptable, Vorssaint plus a small native-Space app is the focused alternative. Existing Raycast remains a candidate Fn front end, subject to checking its installed version. WhichSpace's downloaded-binary signing/notarization was not independently established. It uses private Apple APIs for window movement, so future OS compatibility remains a practical limitation even without Dock injection or a documented SIP change.

Concrete higher-friction cases:

- **mimi:** beta, ad-hoc signed/not notarized. **InstantSpaceSwitcher** unsigned; **HopTab**, **WinMux** and **1Piece** unnotarized. A fresh release date does not resolve these install-policy questions.
- **1Piece:** author explicitly has not tested macOS26+, despite the October2026 release.
- **rcmd:** required Screen Recording for current window switcher, not simply an optional preview feature.
- **skhd.zig:** ordinary hotkey event-tap mode differs from optional tap-hold/root grabber/DriverKit mode. The latter is a much bigger corporate installation decision; do not conflate them.
- **yabai:** basic operation is not universally SIP-dependent. The advanced scripting-addition path is the one with partial SIP changes and Dock injection.
- **omacosy/Omacchiato:** complete themed environments including Karabiner and multiple helper permissions, much broader than replacing app hotkeys and manual window controls.

Existing OmniWM is signed/notarized according to its stable documentation and uses SIP-on operation, but its own workspace layer still conflicts with the stated native-desktop preference. Corporate compatibility and workspace semantics are independent considerations.

## What a focused trial should verify

The research is complete; a migration would be separate work. A small reversible trial should check the following before changing all27 bindings:

1. Check Vorssaint's Command Bar app hotkeys, saved-script hotkeys and Window layout with supported modifier chords. Decide whether preserving every existing Fn layer is essential before replacing its input engine.
2. Invoke WhichSpace's numbered switch and front-window move actions from a Vorssaint saved executable script; confirm the desired stay/follow behavior, monitor handling and existing native desktop numbering. This combination is a proposed integration, not a runtime-verified result.
3. If Fn fidelity is required, record Fn+Return, Fn+Shift+Return, Fn+Control+Return and Fn+Option+F in the installed Raycast version before migrating those bindings. Live docs currently describe2.8, while2.4.1 is installed. Also verify native/manual size controls and the Ghostty+Herdr script launch.
4. Separately account for BTT-specific cheat-sheet behavior, Stage Manager cycling and **Quit App Under Cursor**. A generic frontmost-app quit command is not equivalent to quitting the app under the mouse.
5. Verify the permitted installation/permission route for any added tool. No Gatekeeper/SIP bypass was performed or proposed as a necessary migration step.

## MangoWC / MangoWM clarification

The recollected tool is indeed Linux-oriented. The current official project is [mangowm/mango](https://github.com/mangowm/mango), the **Mango Wayland Compositor**, based on dwl/wlroots, with installation documentation for Linux distributions. The old DreamMaoMao/mangowc project points there. No native macOS edition is documented. [Official installation guide](https://mangowm.github.io/docs/installation).

## Detailed evidence reports

- [Hotkeys, launchers and automation](2026-10-14-hotkey-tools.md): first-party pricing, Fn behavior, permissions, release histories.
- [Native/manual window tools](2026-10-14-native-window-tools.md): stable versus prerelease features, sizing/layouts, native desktop distinctions, install facts.
- [Integrated tools and Spaces managers](2026-10-14-integrated-and-spaces-tools.md): WhichSpace release-tag/source checks, recent projects, workspace models, Mango clarification.
- [Native macOS foundation and local verification](2026-10-14-native-macos-foundation.md): actual OS/app versions, Apple's built-in controls, research limits.
- [Vorssaint source-level follow-up](2026-10-14-vorssaint-deep-dive.md): corrects the initial omission of shipping app/script hotkeys and identifies the actual Fn/native-Space gaps.
- [OmniWM and dedicated Omarchy stacks](2026-10-14-omniwm-and-omarchy-stacks.md): audited installers/configuration, modular Macoma, and current local OmniWM settings.
- [Native macOS26 versus Golden Gate27](2026-10-14-native-macos-26-vs-27.md): official version comparison, native-only capability limits and upgrade relevance.

Discovery used web searches, followed by first-party product pages, tagged source and release histories. Anonymous Tavily search and GitHub API rate caps constrained discovery requests; direct official-source collection continued. Context7 was used for current Hammerspoon API docs. Its mimi lookup returned unrelated libraries, which were rejected; mimi facts are from its author's tagged docs. None of the feature comparisons rely on unverified training knowledge, and no unknown YouTube video is claimed to have been identified.
