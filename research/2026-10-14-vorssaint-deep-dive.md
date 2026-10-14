# Vorssaint 3.4.1: remaining Omarchy-on-Mac gaps

**Live follow-up:** [native Fn+1–5 desktop switching](2026-10-14-native-fn-desktop-test.md) is now configured and verified independently of Vorssaint or BTT. A companion is therefore unnecessary for desktop navigation alone. Vorssaint's own Fn model and direct numbered window-transfer gaps remain as described below.

**Window-transfer follow-up:** [WhichSpace directly handles Fn+Shift+1–5](2026-10-14-whichspace-fn-move-test.md) after setting its saved bindings outside the recorder. The user confirmed physical moves with Fn+Shift+1/Fn+Shift+2. A Raycast/BTT/Vorssaint script bridge is unnecessary for those transfers. Vorssaint's own Fn limitations still apply to actions assigned within Vorssaint.

Research date: 2026-10-14. This report keeps Vorssaint as the preferred foundation. It distinguishes shipping behavior in the user's installed version from requests, newer development changes, and combinations that need testing.

## Evidence and local state

The installed `/Applications/Vorssaint.app/Contents/Info.plist` identifies version **3.4.1**, build **101**, bundle ID `com.vorssaint.utils`, minimum macOS **14.0**. The official release is dated October 8, 2026. The source is publicly available, GPL-3.0-or-later; it is not a binary-only project. I read a checkout pinned to tag `v3.4.1`, commit `aea106cb5d52045c99810cf672da891d2a20b67d`, alongside the installed app's bundled changelog. Source-only findings are not runtime tests. [1][2]

Read-only inspection of `~/Library/Preferences/com.vorssaint.utils.plist` found these feature-availability values false: **Command Bar, Window layout, Maximize windows, Super key, Mouse button shortcuts, App switcher, Dock Preview**. Command Bar app-hotkey and saved-script settings were absent. These are **in-app module install/availability flags**, not a statement about missing product capabilities or denied permissions. The source explicitly defines availability as a layer above each feature's own enable setting: an unavailable module disappears from Settings and stops its service, with saved settings preserved. The Features hub's Install operation toggles bundled feature availability; it is not a separate plugin download. No settings were changed. [3]

## Main conclusion

**Vorssaint already ships substantially more of this workflow than the broad comparison established.** Version 3.4.1 supports direct app hotkeys, direct custom-script hotkeys, extensive window-placement hotkeys, customizable Super-key output, and native Space-aware window switching/dragging.

The two significant gaps for reproducing this particular preset are:

1. **Fn/Globe is not supported as a global hotkey modifier or Super-key source in 3.4.1.** This is established by the actual shortcut model and source-key enum, not just missing documentation.
2. **Direct keyboard commands to switch to Desktop 1–4 or send the focused window to Desktop 1–4 are not exposed as shipping Vorssaint actions.** Space-aware focusing and dragging a window from another desktop are different features. Native Space-navigation actions remain an open request.

An additional integration gap: Vorssaint currently has no public incoming command interface through URL schemes, AppleScript, Apple Shortcuts actions, or a general-purpose control CLI. Its saved scripts can nevertheless invoke external helpers, so this does not prevent a small companion solution. [4][5][6][7][8]

## Capability matrix

| Requested capability | Shipping in 3.4.1? | Exact evidence / practical meaning |
|---|---|---|
| Launch or focus Ghostty, Chrome, Zed, Finder, Calendar, Mail, Calculator, 1Password using dedicated global hotkeys | **Yes** | Settings → Command Bar → **App shortcuts**. UI caption: “Open apps with their own shortcuts, even when the bar is closed.” App hotkeys run without opening the bar, including before the bar was opened that session. [4] |
| Repeat an app hotkey to hide/show it | **Yes** | If the target app owns the frontmost window, its hotkey hides it; otherwise it launches/raises/opens a window. Next press brings it back. This is a deliberate toggle, not necessarily the exact focus-only behavior of the BTT preset. [4] |
| Repeat an app hotkey to cycle its windows | **Not established as this app-hotkey behavior** | Existing app hotkeys toggle hide/show. An open October 11 request asks for fixed app-number assignments with repeated-key window cycling. App Switcher has separate window cycling. [18] |
| Arbitrary global hotkeys to built-in commands and saved items | **Yes, within the shortcut model** | Command Bar rows can have their own global shortcut through **Give it a shortcut**. The source limit is **64** row shortcuts, covering app and other rows. The old 20 limit was raised; issue #2091 is closed. Prompt-requiring actions still open the bar/confirmation. [4][9][17] |
| Dedicated hotkey to run a custom local script silently | **Yes** | Add a saved **Script**, choose an executable file, and enable **Run from its global shortcut without opening the bar**. With its own row shortcut assigned, it executes immediately with **no argument** and displays no result. The script source calls `Shell.run` on the executable path, not an inline shell command pasted into the hotkey field. [10][11] |
| Ghostty running Herdr on a dedicated hotkey | **Supported building block; wrapper unbuilt/untested** | A saved executable script can perform the existing Ghostty launch operation and receive a direct global shortcut. A long-lived terminal session should be launched rather than run inside the bounded Command Bar script runner. No wrapper was written or executed during this research. [10][11] |
| Fn+Return, Fn+Shift+Return, Fn+Control+Return as distinct native Vorssaint hotkeys | **No** | `GlobalShortcutModifiers` includes only Control, Option, Shift, Command. Its valid mask, serialized tokens, Carbon flags, CGEvent conversion and NSEvent conversion do not include Fn. Entering Fn in serialized preferences would not add support; its parser rejects unknown modifier tokens. [5] |
| Fn/Globe as the source of Vorssaint's Super key | **No** | `SuperKeySource` is exactly Caps Lock, Right Command, Right Option, Right Control, Right Shift. No Fn/Globe case. [6] |
| Choose what modifiers Super produces | **Yes** | Output is any selected combination of Control/Option/Shift/Command containing at least one of Control/Option/Command. Default is all four. Can omit Shift, or choose a smaller combination; cannot output Fn. [6][16] |
| Preserve all extra Shift/Control/Option layers through a Hyper substitute | **Not equivalent** | If Super already emits a modifier, additionally holding that modifier cannot create a distinct layer. Omitting Shift leaves a separate Shift layer, but Control/Option layers remain consumed if they are part of the output. A one-modifier output leaves more layers but shares ordinary macOS shortcuts; it is not an isolated Fn-based Super. [5][6] |
| Native window half/third/quarter/sixth placements, centering, maximize, restore | **Yes** | `WindowLayoutAction` exposes an extensive preset list, per-action shortcut rows and restore. Maximize fills a screen while fullScreen is a separate action. Adjustable-margin maximize and repeated-side cycling are available. [7] |
| Native macOS tiling specifically, versus changing window frames | **Partly / distinguish the mechanism** | Window layout uses Accessibility to resize/reposition existing windows; Full Screen is separate. The green-button maximizer keeps a normal window on its current Space. Edge snapping deliberately defers while conflicting macOS system tiling settings are active. This preserves native desktops but is not proof every placement uses Apple's native tiled-window groups. [7][12] |
| Arbitrary custom pixel X/Y/width/height presets | **Not found in the shipping settings/action model** | Extensive enumerated placements and adjustable margin exist; no arbitrary user-defined frame action surfaced in the inspected settings. A local script could provide custom positioning, with behavior depending on the external implementation. [7] |
| Move windows between monitors/displays | **Yes** | Previous Display and Next Display are explicit actions. **Displays are not Spaces.** [7] |
| Focus a window on another Mission Control Space | **Yes** | App Switcher/Command Bar/Dock Preview enumerate other desktops and activate those windows; the source has private window-server Space topology and Space-hop support. [8] |
| Drag a preview from another desktop onto the currently visible desktop | **Yes** | Dock Preview can drag a thumbnail to a location and preserve its size; `moveToVisibleSpace` carries the window to the Space currently visible under the pointer. This is not a command to send the active window to any numbered desktop. [8] |
| Keyboard previous/next/jump-to-numbered native Space actions | **Not exposed as dedicated shipping actions** | Mouse-button drag gestures already request adjacent native Space movement. The explicit keyboard/Command Bar/radial-menu Previous/Next/Jump feature request remains open (#1159). [13] |
| Send focused window to native Desktop 1–4 by hotkey | **No exposed shipping action found** | No numbered-Space action appears in `WindowLayoutAction` or Command Bar action inventory; private Space movement source is used for visible-Space preview dragging. A native Spaces companion is the appropriate gap filler. [7][8][13] |
| Preserve native desktop numbering/order | **Yes, separate setting** | Fixed Space order disables macOS's recent-use reordering; this does not add numbered send/switch commands. [1][2] |
| Saved scripts call external AppleScript / Apple Shortcuts / helper tools | **Supported direction, with wrappers** | Vorssaint runs local executable files; these can invoke other applications/tools under the user account. Link destinations can open another app's URL scheme. This is **Vorssaint driving external tools**, not external automation controlling Vorssaint. [10][11] |
| External URL/AppleScript/Shortcuts/CLI controls Vorssaint's internal actions | **Not shipping public interface** | No URL scheme registration/AppIntents/control scripting interface found in pinned source. Incoming deep links, AppleScript parameters and CLI/Shortcuts read/write actions are consolidated in open #514. App entry-point flags are test/sensor/uninstall utilities, not a window-management control API. [14] |
| Automatically import a directory of Raycast-style script commands | **Requested, not shipping** | Open issue #1178 proposes directory indexing, Raycast headers, richer argument/output modes. Individual saved executable Script items already work. [15] |

## How to use the built-in pieces without replacing Vorssaint

These are setup instructions derived from the shipping UI/source; I did not perform them.

1. In **Settings → Features**, install **Command Bar** and **Window layout** individually. Install **Super key** only if a Caps Lock/right-side modifier source is desirable. A first feature install can turn on its primary control, so review its shortcuts before using it. The local preference flags show these pieces were not installed inside Vorssaint when inspected. [3]
2. Use **Settings → Command Bar → App shortcuts** to assign supported modifier chords to common apps. This is more direct than opening Command Bar and typing the app name each time. The app shortcut remains active when the bar is closed; it does not depend on enabling the bar's own opening hotkey. [4]
3. Give Window layout's handful of useful placements their own shortcuts. For the current BTT “fill screen” action, compare **Maximize** against native **Full Screen**; they are distinct in Vorssaint. [7]
4. For special launch actions, use **Command Bar → Your shortcuts → Add shortcut → Script**, select an executable file, enable **Run from its global shortcut without opening the bar**, then assign the saved row a shortcut via **Give it a shortcut**. This can launch a Ghostty/Herdr wrapper or invoke a native Spaces helper. [10]
5. Keep mission-critical Fn-layer migration separate from the above adoption: Fn combinations are unsupported by the 3.4.1 model. Retaining the existing Fn hotkey engine temporarily is a small bridge; abandoning Vorssaint's other features is unnecessary.

## Minimal companion choices

### If preserving Fn/Globe is essential

Keep Vorssaint for its utilities, window placement and previews. Use the already-installed **Raycast** as the Fn-capable app/script hotkey layer, subject to checking the installed version against the current manual. Current Raycast docs explicitly demonstrate `fnA` and `fnCtrlA`. Use a native Spaces helper such as **WhichSpace** for numbered switch/send operations. The parent investigation separately verified WhichSpace integrations; no combination was tested here. [19]

Without a public Vorssaint command API, Raycast cannot directly invoke a Vorssaint internal placement by a documented URL. A Fn bridge could simulate a supported shortcut assigned to a Vorssaint action, but this remains an **untested bridge**, not a proven integration. Alternatively, have the Fn engine perform that small window action itself while Vorssaint continues to provide the preferred experience.

The smallest immediate change is to retain BetterTouchTool only for the unsupported Fn and numbered-Space bindings while moving app and window features into Vorssaint as desired. Removing BTT completely can wait until the representative chords and helper interactions have been tested.

### If changing the Super key is acceptable

Vorssaint can own app hotkeys, script hotkeys and window placement directly using Caps Lock or a right-side modifier. Add **only a native Spaces helper** for Desktop 1–4 send/switch, invoked from saved scripts/links where its interfaces permit. Carefully choose Super output: the default all-four Hyper consumes the user's extra Shift/Control/Option layers. A three-modifier output preserves Shift only; a one-modifier output risks ordinary shortcut collisions. [6]

Apple Shortcuts can serve as an intermediate action runner when useful, but it does not make Fn an available modifier in Vorssaint and does not itself provide a general supported native “send window to desktop N” action established by this research.

## Open requests and development status

- **#1159 — native Space navigation/instant transitions:** open. A contributor says existing mouse drag already navigates native Spaces and regular Previous/Next/Jump actions would be an extension. The same discussion separates actual native desktops from managers with their own workspaces. This is a request, not a shipping commitment. [13]
- **#514 — external automation:** open. It consolidates deep links, AppleScript, terminal commands, Shortcuts actions, parameters and reading values back. Its scope is directly relevant to using Raycast/Shortcuts as a clean Fn bridge. [14]
- **#1178 — script folder discovery:** open; relevant convenience, but not a reason to overlook existing individual scripts. [15]
- **#2164 — safe application of externally edited preferences:** open. It describes some settings requiring restart and writes potentially being overwritten. It supports using the app's configuration/import UI instead of changing plist keys blindly. [20]
- **#594 — customizable Super output:** closed as completed; code confirms it ships. [16]
- **#926 — choose Caps Lock/right-side Super source:** closed; code confirms those five sources ship. Fn is not among them. [21]
- **#2091 — old 20-app-shortcut limit:** closed; pinned code confirms 64. [17]
- **#2676 — instant Fn language switching:** open, but it concerns language switching rather than arbitrary global Fn hotkeys. It does not establish a plan to support the user's layered Fn bindings. [22]
- **#2971 — stable app-number hotkeys with window cycling:** open; its extra cycle behavior differs from existing launch/hide/show app hotkeys. [18]

No public `ROADMAP.md` was found at the checked path; the actual issue state and release source are better evidence than assuming a requested feature is scheduled. Main-branch CHANGELOG includes an Unreleased section beyond installed 3.4.1; I did not credit those changes as installed behavior.

## macOS 27 / Golden Gate upgrade relevance

Vorssaint 3.4.1 contains deliberate macOS 27 support, rather than only an old minimum-version claim. Its release notes describe per-app AirPlay routing on macOS 27+, a fix for Siri AI unexpectedly opening Settings on macOS 27, and window capture including sheets on macOS 27. Pinned source has an explicit `#available(macOS 27, *)` guard for AirPlay and a macOS 27 Stage Manager window-preview handling comment. These establish that the developer was addressing macOS 27 behavior in this release. They do **not** establish a successful runtime test of the user's hotkeys after upgrading. [2][23]

The unsupported Fn modifier and absent numbered desktop actions are application-model gaps in 3.4.1; installing a newer macOS does not, by itself, add cases to Vorssaint's shortcut model or expose missing actions. Native macOS improvements can reduce companion needs independently, which the parent research assesses separately. A concrete upstream issue reports intermittent Super-key window-layout activation on macOS 27 with Vorssaint **3.3.5** (#1865); it remains open, but it is not proof that installed 3.4.1 is affected. Treat it as a representative check to perform if adopting Caps Lock Super on macOS 27, not as a reason to declare Vorssaint incompatible. [5][6][24]

## Permissions and corporate-Mac fit

Window layout needs **Accessibility**. Window previews need **Screen Recording**; declining recording falls back to app icons in the switcher. Normal app launch hotkeys use Carbon registrations and do not intrinsically require a screen-capture grant. Scripts may request whatever permissions their actions need, such as Automation when sending Apple Events. Super key remaps through `hidutil` and event taps; there is no keyboard-driver installation or SIP-reduction step in its source/install flow. Fan control and closed-lid features have separate administrator/helper paths and should not be conflated with app/window hotkeys. Existing Vorssaint installation and ordinary permission flows do not prove company approval. [12]

## Sources

All code links are pinned to the user's installed `v3.4.1` release unless explicitly labeled an issue/current external document.

1. Official stable release: https://github.com/vorssaint/vorssaint-utils/releases/tag/v3.4.1
2. Pinned feature overview/release history: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/README.md and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/CHANGELOG.md
3. Feature availability semantics and Install implementation: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Core/FeatureCatalog.swift#L6 and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/App/FeatureRuntime.swift#L98
4. App shortcut UI/runtime: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/UI/Settings/CommandBarAppShortcutsView.swift and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/CommandBar/CommandBarService.swift#L834
5. Exact global modifier representation/storage/event conversions: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Core/GlobalShortcut.swift#L9
6. Super source keys, output combinations, validation and HID mapping: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/SuperKey/SuperKeySupport.swift
7. Window action catalog and settings: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/WindowLayout/WindowLayoutSupport.swift#L28 and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/UI/Settings/WindowLayoutSettings.swift
8. Native Spaces topology and visible-desktop movement: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/Switcher/SpaceWindowBridge.swift and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/Switcher/SpaceHop.swift
9. Global row hotkeys, toggle logic and 64 limit: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/CommandBar/CommandBarRowShortcuts.swift#L13
10. Saved scripts/links/direct-execution UI: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/CommandBar/CommandBarLinks.swift#L13 and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/UI/Settings/CommandBarSettings.swift#L570
11. Script runner/direct run: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/CommandBar/CommandBarScriptRunner.swift and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/CommandBar/CommandBarCatalog.swift#L1458
12. Permission guide: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/docs/PERMISSIONS.md
13. Native Space navigation request: https://github.com/vorssaint/vorssaint-utils/issues/1159
14. Incoming command integrations request plus pinned registrations/entry point: https://github.com/vorssaint/vorssaint-utils/issues/514 and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Resources/Info.plist and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/main.swift
15. Raycast-style scripts folder request: https://github.com/vorssaint/vorssaint-utils/issues/1178
16. Custom Super output shipped: https://github.com/vorssaint/vorssaint-utils/issues/594
17. Global row-shortcut capacity raised: https://github.com/vorssaint/vorssaint-utils/issues/2091
18. App number/window-cycle request: https://github.com/vorssaint/vorssaint-utils/issues/2971
19. Current Raycast Fn modifier docs: https://manual.raycast.com/command-aliases-and-hotkeys
20. External preference edits/import request: https://github.com/vorssaint/vorssaint-utils/issues/2164
21. Alternative Super source keys shipped: https://github.com/vorssaint/vorssaint-utils/issues/926
22. Fn language switching request: https://github.com/vorssaint/vorssaint-utils/issues/2676
23. Pinned macOS 27 AirPlay guard/window-preview handling: https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/Audio/AirPlayRouteManager.swift#L80 and https://github.com/vorssaint/vorssaint-utils/blob/v3.4.1/Sources/Vorssaint/Services/Switcher/WindowPreviewProvider.swift#L97
24. Specific reported 3.3.5/macOS 27 Super-key window-layout issue: https://github.com/vorssaint/vorssaint-utils/issues/1865

No apps, shortcuts, permissions, preference files or company settings were changed. The pinned source checkout was downloaded to `/tmp` for inspection; the research report is the only added project artifact.
