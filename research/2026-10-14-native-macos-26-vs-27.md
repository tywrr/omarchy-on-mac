# Native-only Omarchy-style controls: macOS 26 versus 27

**Live follow-up:** native **Fn+1–5 desktop switching is now configured and verified working on macOS26.7.1**, with BTT absent. The user confirmed physical Fn+1/Fn+2; synthetic Fn+3–5 changed actual native Spaces. A fifth desktop was created through Mission Control. See [implementation and verification](2026-10-14-native-fn-desktop-test.md). This resolves the desktop-navigation Fn question below; generic Apple Shortcuts Fn recording and numbered window transfers remain separate questions. The research snapshot below predates that implementation.

Researched 14 October 2026 against Apple Support, version-pinned Apple user guides, and read-only resources bundled with the local macOS installation. No shortcuts, apps, permissions, or OS versions were changed.

## Conclusion

**Most of the foundation is already achievable with native macOS 26.7.1: global app-launch hotkeys through Apple Shortcuts, keyboard window tiling, and Mission Control desktop navigation. Upgrading to macOS 27 does not establish a solution to the two meaningful remaining gaps: preserving every custom Fn/Globe chord and a direct built-in keyboard action to send the active window to Desktop 1–4.** Custom AppleScript/UI automation could potentially implement missing behaviors using native components, but that is a scripting project requiring verification, not a newly documented macOS27 feature.

Apple's six relevant window-management topics have identical main content in their version26 and version27 editions: Spaces, Mission Control, tiling UI, tiling keyboard table, App Shortcuts, and Stage Manager. This establishes documentation parity for these workflows, not proof that all performance, visual, or undocumented behavior is identical.

## Is Golden Gate real and current? Is this Mac eligible?

Yes. Apple calls **macOS 27 Golden Gate** the latest major Mac operating system, released **14 September 2026**. The latest stable point release listed by Apple's security releases page is **27.0.1, released 28 September 2026**. The OS is a public release; **Siri AI** is separately described as beta/rolling out. Do not conflate those statuses. Apple lists **26.7.1 on the same 28 September date** for the retained Tahoe line. [Release security document](https://support.apple.com/en-us/149035), [current version and dated releases](https://support.apple.com/en-us/100100), [Golden Gate update notes](https://support.apple.com/en-us/127257).

Golden Gate supports **Apple-silicon Macs**, including M-series and A-series; Intel Macs are excluded by the published compatibility list. Read-only local verification reports model **Mac15,12**, and the parent investigation reports `hw.optional.arm64 = 1`. Apple's model-identification page maps Mac15,12 to **MacBook Air (13-inch, M3, 2024)** and explicitly lists macOS27 as its newest compatible OS. The hardware is eligible; this does not establish when the employer wants this Mac upgraded. [Compatibility list](https://support.apple.com/en-us/127255), [upgrade guide](https://support.apple.com/en-us/127455), [MacBook Air identification](https://support.apple.com/en-us/102869).

## Feature matrix

| Requirement | Native macOS26 | Native macOS27 | Remaining practical issue |
|---|---|---|---|
| Global shortcut opening Ghostty, Chrome, Zed, Finder, Calendar, Mail, Calculator | Apple Shortcuts can bind a shortcut to a key combination that runs **in any app**; use an Open App action | Same documented keyboard mechanism | Exact custom Fn/Globe acceptance not verified; reserved system shortcuts cannot be overridden |
| Open Ghostty running Herdr, with arguments/working directory | Shortcuts Run Shell Script provides a native automation host; exact installed Ghostty/Herdr invocation must be checked | No documented need to upgrade for this | Open App alone does not supply terminal command arguments; script/action behavior needs a small test |
| Spotlight launcher and quick keys | Already has Actions, quick keys, and clipboard search in26 | Adds Siri AI conversational actions/personal context | Quick keys are typed **inside Spotlight**, then Return; they are not simultaneous global Fn hotkeys |
| Fill, center, left/right/top/bottom halves | Native Fn-Control-F/C/arrows | Same documented table | User can accept defaults or configure native shortcut settings; target app must support native behavior |
| Individual quarters and four-window quarter arrangement | Native menu actions; no default shortcut, but local Windows preferences contain configurable actions | Same documented menu/default-shortcut table | “n/a” in Apple table means no default shortcut, not absence of the action |
| Custom keyboard menu actions | App Shortcuts / All Applications can bind existing menu commands | Same documented mechanism | Only menu commands; not a general app-launch shortcut facility |
| Native desktops, next/previous desktop | Mission Control; Control-Left/Right, configurable in Keyboard settings | Same documented mechanism | Desktop ordering/available desktop settings need normal setup |
| Jump to numbered native desktops | Local Apple KeyboardSettings resources contain Switch to Desktop1–16 labels | No new mechanism established by27 docs | Exact Fn+1–4 rebindings need recorder/settings verification; actual desktops must exist |
| Send the active window to numbered Desktop1–4 using one shortcut | Apple's documented window-move operations are dragging to screen edge or Mission Control thumbnail | Same documentation; no built-in direct send action established | **Meaningful native UI gap** for user's Fn-Shift-1–4. Dock Assign To is per-app assignment, not a per-window keyboard send |
| Window coordinates/custom arbitrary size/layout sequence | Native automation can compose actions/scripts; AppleShortcuts supports automation and scripts | No requirement to upgrade established | Exact built-in Find Windows/Move Window/Resize Window action parameters not verified in this run; scripts remain possible |
| Toggle Stage Manager | Native Keyboard settings resource has Turn Stage Manager on/off, unset default | Same Stage Manager documentation | Optional, since user's toggle currently disabled |
| Cycle Stage Manager stages with Option-Tab / Option-Shift-Tab | Built-in stage-cycle equivalent not established from reviewed sources | Not added in reviewed27 documentation | Cmd-Tab switches apps; it should not be presented as the same stage-cycle command |
| Quit app under mouse, Fn-W | Standard Cmd-Q quits active/frontmost app | Same native distinction | Under-pointer semantics would need automation; not equivalent to active-app quit |
| Lock, show notification center, show app launcher | Native keyboard commands exist | Native commands still exist | Exact user's custom Fn chords may differ; Fn-N and Fn-Shift-A are documented native alternatives |

Sources for rows: [Shortcuts26 keyboard-run guide](https://support.apple.com/guide/shortcuts-mac/apd163eb9f95/9.0/mac/26), [Shortcuts27 guide](https://support.apple.com/guide/shortcuts-mac/apd163eb9f95/10.0/mac/27), [native tiling26](https://support.apple.com/guide/mac-help/mchl9674d0b0/26/mac/26), [native tiling27](https://support.apple.com/guide/mac-help/mchl9674d0b0/27/mac/27), [Spaces26](https://support.apple.com/guide/mac-help/mh14112/26/mac/26), [Spaces27](https://support.apple.com/guide/mac-help/mh14112/27/mac/27), [App Shortcuts26](https://support.apple.com/guide/mac-help/mchlp2271/26/mac/26), [App Shortcuts27](https://support.apple.com/guide/mac-help/mchlp2271/27/mac/27), [Mac keyboard commands](https://support.apple.com/en-us/102650). Local source details below.

## App launch hotkeys and Spotlight are different systems

Apple's Shortcuts guide gives a true global keyboard route: open a shortcut, choose Details, click **Add Keyboard Shortcut**, and press a combination. It says: “**In any app in macOS, press the key combination.**” It also says some shortcuts are reserved for system use. This paragraph appears in both the pinned macOS26 and27 guides. A separate shortcut containing Open App can launch each chosen app; a native scripting action can cover terminal launch arguments or workflows with several steps. [26 guide](https://support.apple.com/guide/shortcuts-mac/apd163eb9f95/9.0/mac/26), [27 guide](https://support.apple.com/guide/shortcuts-mac/apd163eb9f95/10.0/mac/27).

By comparison, Spotlight quick keys are command abbreviations such as `ft Ashley`: first open Spotlight with Command-Space, type the abbreviation/arguments, and press Return. They already existed in Tahoe26. macOS27 adds SiriAI interactions and extra actions, but those do not establish new simultaneous global app-launch keys. [Spotlight actions26](https://support.apple.com/guide/mac-help/mchl4953dfeb/26/mac/26), [Spotlight actions27](https://support.apple.com/guide/mac-help/mchl4953dfeb/27/mac/27), [Tahoe release notes](https://support.apple.com/en-us/122868).

**Fn caveat:** Apple's native tiling defaults visibly use Fn, and local system shortcut metadata carries Fn-based defaults. That does not prove that Apple Shortcuts' generic recorder accepts Fn+Return, Fn+Shift+F, or all the user's exact chords. The public guide only says “key combination” and doesn't enumerate Fn. No temporary shortcut was created to test this, so Fn fidelity remains unverified, rather than declared impossible or supported.

**App Shortcuts caveat:** System Settings > Keyboard > Keyboard Shortcuts > App Shortcuts customizes existing menu items. Apple explicitly says it cannot create a shortcut for a general-purpose task such as opening an app. App launches should use Apple Shortcuts, not this similarly named preferences section. [Apple App Shortcuts guide](https://support.apple.com/guide/mac-help/mchlp2271/26/mac/26).

## Practical native-only layout on the current Mac

1. **App launches:** create one Apple Shortcuts shortcut per app using Open App, and assign a tested global key combination. If Fn cannot be captured faithfully, a consistent Control-Option family is a possible native substitute. Examples could be Control-Option-Return for Ghostty and Control-Option-Shift-Return for Chrome, subject to conflict checks. These are proposed mappings, not changes made here.
2. **Herdr terminal workflow:** use native Shortcuts scripting rather than merely Open App. Run Shell Script is present in the installed Apple ActionKit resources. Shortcuts > Settings > Advanced > Allow Running Scripts is Apple's documented setting for scripts. The actual Ghostty/Herdr arguments and working directory must be verified against their installed versions when implementing; no command was invented or run here. [Advanced settings26](https://support.apple.com/guide/shortcuts-mac/apdfeb05586f/9.0/mac/26), [Advanced settings27](https://support.apple.com/guide/shortcuts-mac/apdfeb05586f/10.0/mac/27).
3. **Window sizing:** use System Settings > Keyboard > Keyboard Shortcuts > **Windows** for Fill, Center, Halves, Quarters, and Arrange. Local Apple resources verify this pane and quarter actions on the existing26 installation. Default Fill is Fn-Control-F, Center Fn-Control-C, halves Fn-Control-arrows, and two-window arrangements add Shift. Quarters have no default key. App Shortcuts can be an additional route for menu commands where needed. Filling the desktop is different from entering full-screen and creating another Space.
4. **Desktops:** create four native Mission Control desktops and configure Keyboard Shortcuts > Mission Control > Switch to Desktop1–4 plus next/previous actions. Keep a deliberate desktop order; verify Fn+1–4 recording if preserving that exact muscle memory is required.
5. **Moving windows between desktops:** accept Apple's native drag operation, or build/test an AppleScript/UI-automation workaround. Dock > Options > Assign To > This Desktop can pin an app's behavior but is not a direct window-to-desktop hotkey. A completely native *component stack* could include custom scripts, but it would not provide a turnkey native keyboard equivalent verified in this investigation.

## Evidence from the installed Apple resources

These were read without invoking any action or altering settings:

- `/System/Library/ExtensionKit/Extensions/KeyboardSettings.appex/Contents/Resources/en_GB.lproj/DefaultShortcutsTable.xml`: contains the **Windows** category, Fill/Center/Return to Previous Size, halves, individual quarters, quarter arrangement, and StageManager. Individual quarter actions have unset default keys. Fill and halves have Fn-based modifier defaults. The Mission Control StageManager item uses symbolic action222 and the local English text says **Turn Stage Manager on/off**.
- `/System/Library/ExtensionKit/Extensions/KeyboardSettings.appex/Contents/Resources/DefaultShortcutsTable.loctable`: English entries label **Switch to Desktop1 through16**, Move left/right a space, and Stage Manager toggle. No direct send-window-to-numbered-desktop entry was found in these inspected resources. That is a limited negative finding, not a proof against any possible scripting route.
- `/System/Library/PrivateFrameworks/ActionKit.framework/Versions/A/Resources/Localizable.loctable`: English strings verify the presence of **Open App** and **Run Shell Script**, script permission prompts, and a window-resize failure message. The checked current AppIntents metadata did not expose the classic FindWindows/MoveWindow/ResizeWindow definitions, so their exact parameter choices were not verified. This does not establish that those actions are absent.

## What the upgrade actually adds for this question

Apple27 release notes emphasize SiriAI, Visual Intelligence, better Spotlight/Mail search, **Describe a Shortcut** natural-language shortcut creation, design refinement, and speed/reliability improvements. Easier shortcut creation may help build app-launch workflows, but the global keyboard-run mechanism already exists26. No advertised new direct window-to-desktop command or broad Fn hotkey recorder was found. [Official27 release notes](https://support.apple.com/en-us/127257), [What's new27](https://support.apple.com/guide/mac-help/apd07d671600/27/mac/27).

The six version-pinned core topics compared below had **identical main topic content** after stripping HTML, navigation, and footer and stopping at See Also:

| Topic | macOS26 | macOS27 |
|---|---|---|
| Spaces | [mh14112/26](https://support.apple.com/guide/mac-help/mh14112/26/mac/26) | [mh14112/27](https://support.apple.com/guide/mac-help/mh14112/27/mac/27) |
| Tiling shortcut table | [mchl9674d0b0/26](https://support.apple.com/guide/mac-help/mchl9674d0b0/26/mac/26) | [mchl9674d0b0/27](https://support.apple.com/guide/mac-help/mchl9674d0b0/27/mac/27) |
| Tiling UI | [mchlef287e5d/26](https://support.apple.com/guide/mac-help/mchlef287e5d/26/mac/26) | [mchlef287e5d/27](https://support.apple.com/guide/mac-help/mchlef287e5d/27/mac/27) |
| Mission Control | [mh35798/26](https://support.apple.com/guide/mac-help/mh35798/26/mac/26) | [mh35798/27](https://support.apple.com/guide/mac-help/mh35798/27/mac/27) |
| App Shortcuts | [mchlp2271/26](https://support.apple.com/guide/mac-help/mchlp2271/26/mac/26) | [mchlp2271/27](https://support.apple.com/guide/mac-help/mchlp2271/27/mac/27) |
| Stage Manager | [mchl534ba392/26](https://support.apple.com/guide/mac-help/mchl534ba392/26/mac/26) | [mchl534ba392/27](https://support.apple.com/guide/mac-help/mchl534ba392/27/mac/27) |

Apple's enterprise notes also describe new device-management controls for allowed apps/binaries and consolidated privacy consent, plus PlatformSSO changes. These are relevant to an organization's upgrade rollout, not evidence that the user's Mac currently has a known MDM restriction or that27 solves the hotkey gaps. [Enterprise27 notes](https://support.apple.com/en-us/148830).

**Recommendation:** build and verify the native-only app-launch/window-size/navigation foundation on26.7.1 first. The hardware supports27.0.1 and an upgrade may be desirable for its other improvements, but the reviewed evidence does not justify upgrading specifically to eliminate BTT's Fn-modifier and native-desktop window-transfer roles. No upgrade was attempted.
