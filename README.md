# Omarchy on Mac

An [Omarchy](https://github.com/omacom/omarchy)-inspired keyboard workflow using
**Fn/Globe as Super**, **skhd.zig** for app launches, **WhichSpace** for window
moves and a desktop indicator, and **native macOS Mission Control desktops**.

Fn stays a real modifier. Shift, Control, and Option remain separate layers;
Command keeps its usual macOS shortcuts. This setup does not remap Globe to
Hyper or Right Option.

## Current stack

| Component | Responsibility | Version used for this snapshot |
|---|---|---|
| [skhd.zig](https://github.com/jackielii/skhd.zig) | Global Fn app-launch hotkeys | 0.2.0-7e95d99 (fast) |
| [WhichSpace](https://github.com/gechr/WhichSpace) | Menu-bar desktop indicator and moving windows to numbered desktops | 1.4.1 |
| Native macOS | Mission Control desktops, numbered desktop switching, built-in window tiling | 26.7.1 |
| Herdr | Agent manager launched in Ghostty; optional for other bindings | Existing mise shim |

The current configuration uses ordinary skhd hotkeys. Its optional grabber,
tap-hold remapping, and virtual HID driver are not part of this setup.
BetterTouchTool presets are preserved under [legacy/bettertouchtool](legacy/bettertouchtool/).

## Active shortcuts

**Super = Fn/Globe. Alt = Option.**

| Shortcut | Action | Handler |
|---|---|---|
| Super + Return | Open/focus Ghostty terminal | skhd.zig |
| Super + Control + Return | Start Herdr in a new Ghostty instance | skhd.zig |
| Super + Shift + Return | Open/focus Google Chrome | skhd.zig |
| Super + Shift + Option + B | Open a new Chrome incognito window | skhd.zig |
| Super + Shift + F | Open/focus Finder | skhd.zig |
| Super + Control + Q | Open/focus Calculator | skhd.zig |
| Super + 1–5 | Switch to native Desktop 1–5 | macOS |
| Super + Shift + 1–5 | Move the focused window to Desktop 1–5 and follow it | WhichSpace |

App launches and both Return/keypad-Enter variants were exercised with synthetic
key events. The user physically confirmed desktop switching and window moves
with desktops 1 and 2. Physical confirmation of the six skhd launches is still
pending. See [verification notes](research/2026-10-14-skhd-app-launches.md).

Apple keyboards can turn Fn+Return into keypad Enter. The
[skhd config](skhd/skhdrc) includes both key variants for the three Return bindings.
Repeated Herdr and incognito shortcuts request new instances/windows.

## Files

| Path | Contents |
|---|---|
| [skhd/skhdrc](skhd/skhdrc) | Working app-launch config; copied to `~/.config/skhd/skhdrc` |
| [whichspace/settings.plist](whichspace/settings.plist) | Fn+Shift+1–5 bindings and the explicitly configured menu-bar options |
| [macos/fn-desktops.plist](macos/fn-desktops.plist) | Native Fn+1–5 bindings, symbolic hotkey IDs 118–122 |
| [backups](backups/) | Full live preference exports and skhd snapshots, including machine-specific state |
| [scripts/settings.py](scripts/settings.py) | Back up live settings or restore the portable configuration |
| [config.toml](config.toml) | Existing Herdr configuration; kept at its original path for existing symlinks |
| [research](research/) | Findings, alternatives, and implementation evidence |
| [legacy/bettertouchtool](legacy/bettertouchtool/) | Earlier presets and documentation |

## Set up or restore

Requires macOS, Homebrew, and Python 3. The app bindings expect Ghostty and Google
Chrome in `/Applications`. Herdr expects the existing executable shim at
`~/.local/share/mise/shims/herdr`; change that command if your installation differs.
Calculator and Finder are supplied by macOS.

From the repository root:

```sh
brew install jackielii/tap/skhd-zig
brew install --cask whichspace
open -a WhichSpace
```

Create five ordinary desktops in Mission Control. For stable numbering, turn off
**Automatically rearrange Spaces based on most recent use** in System Settings →
Desktop & Dock → Mission Control.

Preview the differences, then restore:

```sh
python3 scripts/settings.py restore --dry-run
python3 scripts/settings.py restore
skhd --start-service
skhd --status
```

Grant the requested Accessibility permissions to skhd and WhichSpace. This Mac
already has a working skhd event tap. Permission grants and login-item approvals
must be configured on each Mac; they are not restored from these files.

The restore command first saves a full rollback snapshot under `backups/`, copies
the skhd config, and merges the saved WhichSpace keys and native desktop IDs into
the current preferences. Other native shortcuts and machine-specific WhichSpace
settings are preserved. It restarts WhichSpace if it was running, reloads native
settings, and asks an already-running skhd to reload. It does not create desktops.
The restore preview was verified against the live setup; a fresh-Mac restore has
not yet been exercised.

Keep overlapping BTT launch/desktop bindings disabled when using this stack.

## Back up changes

After editing the live skhd config, WhichSpace settings, or these desktop shortcuts:

```sh
python3 scripts/settings.py backup
git diff
```

This saves full `io.gechr.WhichSpace` and `com.apple.symbolichotkeys` exports plus
the live skhd config into a timestamped directory under `backups/`. It also
refreshes the three portable configuration files. Commit the resulting changes
when they represent the setup you want to retain.

Full WhichSpace snapshots include display/Space IDs, updater state, and its
settings-window position. The portable file omits those values. Its appearance
options currently enable click-to-switch, hide-empty-Spaces, and show-all-Spaces.
Unspecified appearance settings continue to use WhichSpace defaults.

## Where the native settings live

- **Switch desktops:** System Settings → Keyboard → Keyboard Shortcuts → Mission Control.
  The UI can show only `1`–`5`, omitting Fn even though it is saved in the binding.
- **Native preference domain:** `com.apple.symbolichotkeys`, under `AppleSymbolicHotKeys`.
  This repo saves IDs 118–122 with the Fn modifier mask `8388608`.
- **WhichSpace bindings:** `KeyboardShortcuts_moveToSpace1` through `moveToSpace5`
  in `io.gechr.WhichSpace`, with Carbon modifier mask `131584` (Fn + Shift).
  The action moves the window and follows it to the destination desktop.

WhichSpace's recorder strips Fn. Re-recording a shortcut in that UI can remove
Fn from the saved binding; restore the repo settings to recover it. The Shortcuts
app is not involved in these desktop or app-launch bindings.

## Herdr configuration

The root [config.toml](config.toml) remains the existing Herdr configuration.
If no config exists on a new Mac, link it from the repository root:

```sh
mkdir -p ~/.config/herdr
ln -s "$PWD/config.toml" ~/.config/herdr/config.toml
```

Its prefix is `Control+Space`, with pane, tab, and workspace shortcuts defined in
the file. The skhd launcher retains the earlier working Ghostty command:

```sh
open -na /Applications/Ghostty.app --args -e "$HOME/.local/share/mise/shims/herdr"
```

## Continuing the migration

Only the shortcuts in the active table are configured by this stack so far.
Editor, Calendar/Mail, lock-screen, adjacent-desktop, cheat-sheet, and additional
window-placement shortcuts from the earlier BTT setup have not been ported here.
Native macOS window-tiling shortcuts remain available separately.

The reference is the [Omarchy hotkeys manual](https://github.com/omacom/omarchy/blob/quattro/manual/07-hotkeys.md).
Current configuration files take precedence over older research recommendations.
