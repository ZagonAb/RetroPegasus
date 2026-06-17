# RetroPegasus Converter Tool

A professional command-line utility for seamless migration from RetroArch to Pegasus Frontend. RetroPegasus automates the conversion of playlists, metadata, and media assets while maintaining compatibility across Windows, Linux, and macOS.

![demo](https://github.com/ZagonAb/RetroPegasus/blob/c4ead06853653f24f4c5feb7ce1fcf8b59a216cd/assets/image/demo.gif)

## ✨ Features

- **Zero Dependencies** - Uses only Python standard library
- **Cross-Platform** - Native support for Windows, Linux, and macOS
- **Intelligent Auto-Detection** - Automatically locates RetroArch installations
- **Interactive Collection Selection** - Choose which systems to convert (all, single, range, or custom combination)
- **Smart Core Handling** - Detects global or per-game cores automatically
- **Flexible Media Handling** - Choose between absolute paths, copy mode, or metadata-only generation
- **Clean Terminal Interface** - ANSI color-coded output for better readability
- **Detailed Logging** - Generates a comprehensive log file with timestamp and statistics
- **Robust Error Handling** - Validates paths and provides clear error messages
- **Batch Processing** - Handles multiple systems in a single execution

## 📋 Requirements

- Python 3.6 or higher
- RetroArch installation with:
  - `playlists` folder containing `.lpl` files
  - `thumbnails` folder (optional, for media assets)

No external packages required. Uses only Python standard library modules.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/ZagonAb/RetroPegasus.git
cd RetroPegasus

# Run the script
python3 RetroPegasus.py
```

## 💻 Supported Operating Systems

### Windows
Automatically detects installations in:
- `%APPDATA%\RetroArch`
- `C:\Program Files\RetroArch`
- `C:\Program Files (x86)\RetroArch`
- `C:\RetroArch-Win32`
- `C:\RetroArch-Win64`

### Linux
Automatically detects installations in:
- `/usr/bin/retroarch`
- `~/.var/app/org.libretro.RetroArch/config/retroarch/` (Flatpak)
- `~/snap/retroarch/current/retroarch` (Snap)
- `~/.config/retroarch`

### macOS
Automatically detects installations in:
- `~/Library/Application Support/RetroArch`
- `/Applications/RetroArch.app`
- `~/Applications/RetroArch.app`

## 📖 Usage Guide

### Step 1: Select RetroArch Source
Choose between automatic detection or manual path specification.

### Step 2: Configure Output Location
Select where to create the Pegasus Frontend data structure.

### Step 3: Select Collections to Convert
After choosing the output folder, you'll see a list of all detected playlists. You can:

- **Process all**: Type `a` or `0`
- **Process specific**: Type numbers separated by commas (e.g., `1,3,5`)
- **Process ranges**: Use hyphens (e.g., `2-4`)
- **Combine**: Mix both (e.g., `1,3-5,7`)

### Step 4: Choose Media Handling Mode
- **Option 1 (Recommended)**: Use absolute paths to existing RetroArch thumbnails
- **Option 2**: Copy images to Pegasus folder structure
- **Option 3**: Skip media entirely (metadata only)

The tool will then generate the necessary `metadata.txt` files for each selected system.

## 🧠 Core Detection Logic

RetroPegasus intelligently handles core assignments:

- **Global Core**: If all games in a playlist use the same core, a single `launch:` line is added at the collection level.
- **Per-Game Cores**: If games use different cores (or if one game uses a different core from the default), each game gets its own `launch:` line, preserving your individual core choices.
- **Fallback**: If no core is defined, `DETECT` is used, letting RetroArch choose automatically.

This ensures maximum compatibility with custom RetroArch configurations.

## 📁 Generated Structure

### With Absolute Paths (Option 1 - Recommended)

```
~/pegasus-frontend/
├── snes/
│   └── metadata.txt
├── megadrive/
│   └── metadata.txt
└── gba/
    └── metadata.txt
```

### With Media Copy (Option 2)

```
~/pegasus-frontend/
├── snes/
│   ├── metadata.txt
│   └── media/
│       ├── boxFront/
│       │   └── game.png
│       ├── screenshot/
│       │   └── game.png
│       ├── logo/
│       │   └── game.png
│       └── titlescreen/
│           └── game.png
├── megadrive/
│   ├── metadata.txt
│   └── media/
│       └── ...
└── gba/
    ├── metadata.txt
    └── media/
        └── ...
```

## 📄 Metadata Format

Each `metadata.txt` file contains:

```ini
collection: Nintendo - Super Nintendo Entertainment System
shortname: snes
launch: retroarch -L /path/to/core.so {file.path}

game: Super Mario World
file: /path/to/roms/Super Mario World.sfc
assets.boxFront: /path/to/thumbnails/Nintendo - SNES/Named_Boxarts/Super Mario World.png
assets.screenshot: /path/to/thumbnails/Nintendo - SNES/Named_Snaps/Super Mario World.png
assets.logo: /path/to/thumbnails/Nintendo - SNES/Named_Logos/Super Mario World.png
assets.titlescreen: /path/to/thumbnails/Nintendo - SNES/Named_Titles/Super Mario World.png
```

## 🎮 Supported Systems

<details>
<summary>Click to expand full list (100+ systems)</summary>

| RetroArch System | Pegasus Shortname |
|-----------------|-------------------|
| Amstrad - CPC | amstradcpc |
| Atari - 2600 | atari2600 |
| Atari - 5200 | atari5200 |
| Atari - 7800 | atari7800 |
| Atari - Jaguar | atarijaguar |
| Atari - Lynx | atarilynx |
| Commodore - 64 | c64 |
| Commodore - Amiga | amiga |
| DOS | dos |
| MAME | mame |
| Microsoft - MSX | msx |
| Microsoft - Xbox | xbox |
| Nintendo - Game Boy | gb |
| Nintendo - Game Boy Advance | gba |
| Nintendo - Game Boy Color | gbc |
| Nintendo - GameCube | gamecube |
| Nintendo - Nintendo 64 | n64 |
| Nintendo - Nintendo DS | nds |
| Nintendo - NES | nes |
| Nintendo - SNES | snes |
| Sega - Dreamcast | dreamcast |
| Sega - Game Gear | gamegear |
| Sega - Genesis/Mega Drive | megadrive |
| Sega - Master System | mastersystem |
| Sega - Saturn | saturn |
| SNK - Neo Geo | ngp |
| SNK - Neo Geo Pocket | ngp |
| Sony - PlayStation | psx |
| Sony - PlayStation 2 | ps2 |
| Sony - PlayStation Portable | psp |
| ...and 70+ more systems |

</details>

## ⚙️ Configuration Validation

The tool validates:
- Existence of RetroArch installation directory
- Presence of required `playlists` and `thumbnails` folders
- Non-empty folder contents
- Valid JSON format in playlist files
- Core path availability (with fallback mechanisms)

## 📝 Logging

A detailed log file `retropegaus.log` is created in the output folder. It includes:
- Timestamped entries
- Playlist processing status
- Core detection results
- Number of games per system
- Total playlists and games processed

The log is overwritten on each new execution for clarity.

## 📜 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIT License © 2026 Gonzalo Abbate (ZagonAb)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software without restriction.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

## 💖 Support

I'm a programming enthusiast passionate about free software and the retro gaming community. All my themes and projects are open-source and freely available. If you find this tool useful, consider supporting its continued development:

[![Support on PayPal](https://img.shields.io/badge/PayPal-0070ba?style=for-the-badge)](https://paypal.me/ZagonAb)
[![Donate using Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/Gonzalo/donate)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-29abe0?style=for-the-badge&logo=ko-fi)](https://ko-fi.com/zagonab)
