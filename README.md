# Omarchy on Mac

Recreating many of the [Omarchy](https://github.com/omacom/omarchy) hotkeys and keyboard-driven workflow on macOS.

---

## Design Philosophy: Approximating "Super" on macOS

This project is an approximation designed to get as close as possible to Omarchy's keyboard-centric workflow on macOS.

### The Problem with macOS Modifiers
In Omarchy (based on Arch Linux + Hyprland), the primary modifier key is **`Super`** (the Windows key). Recreating this on macOS presents unique challenges:

1. **Why not `⌘ Command`?**  
   macOS uses `⌘ Command` for virtually every system and application shortcut (`⌘C`, `⌘V`, `⌘Q`, `⌘W`, `⌘Space`, tab navigation, etc.). Rebinding `Command` breaks fundamental macOS conventions and clashes with deeply ingrained muscle memory.

2. **Why not a "Hyperkey" (`Cmd + Ctrl + Opt + Shift`)?**  
   A popular macOS power-user technique is binding a single key to a "Hyperkey" (all four modifiers pressed simultaneously). While this avoids shortcut collisions, **it completely eliminates Omarchy's modifier layering**. Omarchy heavily relies on layering additional modifiers onto `Super`:
   - `Super + [Key]` (Primary action)
   - `Super + Shift + [Key]` (Secondary or reverse action)
   - `Super + Alt + [Key]` (Alternate mode or secondary application)
   - `Super + Ctrl + [Key]` (System or manager action)  
   Because a Hyperkey already consumes `Shift`, `Alt` (`Option`), and `Ctrl`, you lose the ability to use them as sub-modifiers.

3. **Why not `Caps Lock`?**  
   For long-time Vim users, `Caps Lock` is dedicated to `Escape`. Having `Escape` on the home row is critical for Vim and modal editing.  
   *(Note: For users who don't already map Caps Lock to Escape, using Caps Lock as the modifier—or configuring dual-role tap for `Escape` / hold for a modifier via tools like Karabiner-Elements—is a great alternative).*

### The Solution: `Fn` / Globe via BetterTouchTool
We chose the **`Fn` / Globe key** as our `Super` replacement:
- **Underutilized**: In macOS, `Fn` / Globe is rarely used for primary workflows (mostly dictation or emoji picker).
- **Ergonomic Positioning**: It is located in the bottom-left corner right alongside `Control`, `Option`, and `Command`, making modifier chording natural.
- **Preserves Secondary Modifiers**: With `Fn` as the base modifier, `Shift`, `Option` (`Alt`), and `Control` remain completely independent. You can press `Fn + Shift`, `Fn + Alt`, or `Fn + Ctrl` just like `Super + Shift`, `Super + Alt`, and `Super + Ctrl` in Omarchy.
- **Enabled by BetterTouchTool**: BetterTouchTool natively allows using `Fn` / Globe as a modifier key without requiring low-level system extensions or kernel-level drivers. Other popular utilities (such as [hyperkey.app](https://hyperkey.app), [vorssaint.com](https://vorssaint.com), and similar tools) do not offer `Fn` / Globe as a standalone modifier. While Karabiner-Elements can remap keys, it has limitations with modern macOS `Fn`/Globe handling, and its requirement for system extensions / virtual HID drivers often blocks it on corporate-managed MacBooks under strict MDM policies. BetterTouchTool works cleanly in user space without these hurdles.

---

## Source of Omarchy Hotkeys

The source reference for the hotkeys we are building and porting comes directly from the upstream Omarchy repository:

- **Omarchy Repository**: [https://github.com/omacom/omarchy](https://github.com/omacom/omarchy)
- **Official Omarchy Hotkeys Manual**: [`manual/07-hotkeys.md`](https://github.com/omacom/omarchy/blob/quattro/manual/07-hotkeys.md)
- **Documentation**: [https://learn.omacom.io](https://learn.omacom.io) and [https://omarchy.org](https://omarchy.org)

---

## BetterTouchTool Configuration (`exported_triggers.bttpreset`)

The file `exported_triggers.bttpreset` contains the BetterTouchTool presets, organized into groups matching Omarchy conventions.

### Importing to a New Mac
1. Install [BetterTouchTool](https://folivora.ai/).
2. Open BetterTouchTool -> Click **Presets** in the top-right -> Choose **Import Preset**.
3. Select `exported_triggers.bttpreset` from this repository.

### Current BTT Hotkey Mappings (`Fn` as `Super`)

#### General & Help
| macOS Shortcut (`Fn` / Globe) | Omarchy Counterpart | Action |
| :--- | :--- | :--- |
| `Fn + K` | `Super + K` | Toggle Cheat Sheet |

#### Launching Apps
| macOS Shortcut (`Fn` / Globe) | Omarchy Counterpart | Action |
| :--- | :--- | :--- |
| `Fn + Return` | `Super + Return` | Launch Terminal (Ghostty) |
| `Fn + Shift + Return` | `Super + Shift + Return` | Launch Browser (Safari) |
| `Fn + Ctrl + Return` | `Super + Ctrl + Return` | Launch Herdr (`open -na Ghostty.app --args -e "$HOME/.local/share/mise/shims/herdr"`) |
| `Fn + Shift + N` | `Super + Shift + N` | Launch Editor (Zed) |
| `Fn + Shift + F` | `Super + Shift + F` | Open File Manager (Finder) |
| `Fn + Ctrl + Q` | `Super + Ctrl + Q` | Calculator |
| `Shift + ⌘ + /` | `Super + Shift + /` | Password Manager (Bitwarden) |

#### Navigating & Desktops
| macOS Shortcut (`Fn` / Globe) | Omarchy Counterpart | Action |
| :--- | :--- | :--- |
| `Fn + Tab` | `Super + Tab` | Move Right a Space (Next Desktop) |
| `Fn + Shift + Tab` | `Super + Shift + Tab` | Move Left a Space (Previous Desktop) |
| `Fn + 1` / `2` / `3` / `4` | `Super + 1` / `2` / `3` / `4` | Switch to Desktop 1 / 2 / 3 / 4 |
| `Fn + Shift + 1` / `2` / `3` | `Super + Shift + 1` / `2` / `3` | Move Window to Desktop 1 / 2 / 3 |
| `Fn + W` | `Super + W` / `Super + Q` | Quit / Close app under cursor |
| `Fn + Alt + Space` | `Super + Alt + Space` | Show Apps Menu (Spotlight / Launchpad) |

#### Window Management & Stage Manager
| macOS Shortcut | Omarchy Counterpart | Action |
| :--- | :--- | :--- |
| `Fn + Alt + F` | `Super + Alt + F` | macOS Window Tiling: Fill Screen |
| `Alt + Tab` | `Alt + Tab` | Stage Manager: Cycle Through Stages (Forward) |
| `Shift + Alt + Tab` | `Alt + Shift + Tab` | Stage Manager: Cycle Through Stages (Backwards) |
| `Fn + Shift + Alt + ,` | — | Show Notification Center |

*(Experimental / Under Test)*:
- `Fn + Escape`: Sleep Display (`Super + Escape` System menu)
- `Fn + S`: Stage Manager: Turn Recent Apps On or Off

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
