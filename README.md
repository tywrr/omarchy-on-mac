# Omarchy on Mac

Recreating many of the [Omarchy](https://github.com/omacom/omarchy) hotkeys and workflow on macOS.

## Overview

[Omarchy](https://github.com/omacom/omarchy) is an opinionated Arch Linux distribution (utilizing Hyprland) created by DHH / Omacom. It heavily relies on keyboard-driven workflows using the `Super` key.

On macOS, the `Command` (`⌘`) modifier is already tied to standard macOS application shortcuts. To replicate the Omarchy experience without collisions, we use **BetterTouchTool (BTT)** because it allows configuring the **`Fn` / Globe key** as a modifier. This serves as the macOS equivalent to Omarchy's `Super` key.

This repository tracks:
1. **BetterTouchTool Presets** (`exported_triggers.bttpreset`): Shortcuts and window/app management rules to import on any Mac.
2. **Herdr Configuration** (`config.toml`): Configuration for [Herdr](https://github.com/omacom/omarchy), the terminal/agent manager, symlinked into `~/.config/herdr/config.toml`.

---

## Source of Omarchy Hotkeys

The source reference for the hotkeys we are building and porting to macOS comes directly from the official Omarchy repository:

- **Omarchy Repository**: [https://github.com/omacom/omarchy](https://github.com/omacom/omarchy)
- **Official Omarchy Hotkeys Manual**: [`manual/07-hotkeys.md`](https://github.com/omacom/omarchy/blob/quattro/manual/07-hotkeys.md)
- **Documentation**: [https://learn.omacom.io](https://learn.omacom.io) and [https://omarchy.org](https://omarchy.org)

---

## BetterTouchTool Configuration (`exported_triggers.bttpreset`)

The file `exported_triggers.bttpreset` contains the exported BetterTouchTool triggers.

### Importing to a New Mac
1. Install [BetterTouchTool](https://folivora.ai/).
2. Open BetterTouchTool -> Click **Presets** in the top right -> Choose **Import Preset**.
3. Select `exported_triggers.bttpreset` from this repository.

### Current BTT Hotkey Mappings (`Fn` as `Super`)

| macOS Shortcut (`Fn` / Globe) | Omarchy Counterpart | Action |
| :--- | :--- | :--- |
| `Fn + Return` | `Super + Return` | Launch Terminal (Ghostty) |
| `Fn + Shift + Return` | `Super + Shift + Return` | Launch Browser (Safari) |
| `Fn + Ctrl + Return` | `Super + Ctrl + Return` | Launch Herdr (`open -na Ghostty.app --args -e "$HOME/.local/share/mise/shims/herdr"`) |
| `Fn + Shift + N` | `Super + Shift + N` | Launch Editor (Zed) |
| `Fn + Shift + F` | `Super + Shift + F` | Open File Manager (Finder) |
| `Fn + W` | `Super + W` / `Super + Q` | Quit / Close app under cursor |
| `Fn + Tab` | `Super + Tab` | Move Right a Space (Next Desktop) |
| `Fn + Shift + Tab` | `Super + Shift + Tab` | Move Left a Space (Previous Desktop) |
| `Fn + 1` / `2` / `3` | `Super + 1` / `2` / `3` | Switch to Desktop 1 / 2 / 3 |
| `Fn + Shift + 1` / `2` / `3` | `Super + Shift + 1` / `2` / `3` | Move Window to Desktop 1 / 2 / 3 |

---

## Herdr Configuration (`config.toml`)

The configuration file for `herdr` is maintained in this repository and symlinked to `~/.config/herdr/config.toml`.

### Setting Up Symlink on a New Mac

```bash
mkdir -p ~/.config/herdr
ln -s "$(pwd)/config.toml" ~/.config/herdr/config.toml
```

### Configured Bindings Summary

- **Prefix**: `ctrl+space`
- **Panes**:
  - Split Horizontal: `prefix+h`, `alt+enter`
  - Split Vertical: `prefix+v`, `alt+shift+enter`
  - Close Pane: `prefix+x`, `alt+esc`
  - Zoom Pane: `prefix+z`
  - Focus Pane: `ctrl+alt+left/down/up/right`
  - Resize Pane: `ctrl+alt+shift+left/down/up/right`
- **Tabs**:
  - New Tab: `prefix+c`
  - Rename Tab: `prefix+r`
  - Close Tab: `prefix+k`
  - Switch Tab: `prefix+1..9`, `alt+1..9`
  - Previous / Next Tab: `alt+left`, `alt+right` (or `prefix+p`, `prefix+n`)
  - Move Tab: `alt+shift+left`, `alt+shift+right`
- **Workspaces**:
  - New Workspace: `prefix+shift+c`
  - Rename Workspace: `prefix+shift+r`
  - Close Workspace: `prefix+shift+k`
  - Previous / Next Workspace: `alt+up`, `alt+down` (or `prefix+shift+p`, `prefix+shift+n`)

---

## Omarchy Hotkeys Reference (Target List)

From the [Omarchy Hotkeys Manual](https://github.com/omacom/omarchy/blob/quattro/manual/07-hotkeys.md):

### Navigating & Windows
- `Super + Space`: Omarchy menu (apps and everything else)
- `Super + Alt + Space`: Apps menu
- `Super + Escape`: System menu (suspend, restart, etc)
- `Super + Ctrl + L`: Lock computer
- `Super + W` or `Super + Q`: Close window
- `Ctrl + Alt + Del`: Close all windows
- `Super + T`: Toggle window between tiling/floating
- `Super + J`: Toggle window position (horizontal/vertical)
- `Super + F`: Go full screen
- `Super + 1/2/3/4`: Jump to specific workspace
- `Super + Tab`: Jump to next workspace
- `Super + Shift + Tab`: Jump to previous workspace
- `Super + Shift + 1/2/3/4`: Move window to workspace
- `Super + Arrow`: Move focus to window in direction of arrow
- `Super + Shift + Arrow`: Swap window with another in direction of arrow

### App Launching
- `Super + Return`: Terminal
- `Super + Alt + Return`: Tmux terminal
- `Super + Ctrl + Return`: Herdr (agent manager)
- `Super + Shift + Return`: Browser
- `Super + Shift + F`: File manager
- `Super + Shift + N`: Editor (Neovim)
- `Super + Shift + C`: Calendar
- `Super + Shift + E`: Email
- `Super + Shift + A`: AI
- `Super + Shift + /`: Password manager
