# RetroPegasus Converter Tool

**Your ultimate bridge from RetroArch to Pegasus Frontend**  
Now with a beautiful **Graphical User Interface (GUI)** and full **Command-Line Interface (CLI)** support.

---

## 📌 What's New

- 🖥️ **Modern GUI** built with Tkinter – intuitive, cross-platform, and feature-rich
- 🌍 **Multi‑language support** – English, Español, Português, Français
- 🌗 **Light / Dark themes** – comfortable for any lighting condition
- ✅ **Visual system selection** – checkboxes, select/deselect all, scrollable list
- 📊 **Real‑time progress** – live log, progress bar, and cancel button
- 🧠 **Smarter core handling** – preserves your per‑game core choices automatically
- 🖼️ **Media handling** – absolute paths, copy media, or skip (now fully functional)

---

## ✨ Key Features

- **Zero external dependencies** – only Python standard library (Tkinter is included with most Python distributions)
- **Cross‑platform** – Windows, Linux, macOS all supported natively
- **Automatic RetroArch detection** – finds installations in standard locations
- **Flexible collection selection** – choose all, individual, ranges, or combinations (CLI only)
- **Smart core detection** – handles global and per‑game cores seamlessly
- **Three media modes** – absolute paths (recommended), copy to Pegasus folder, or metadata‑only
- **Rich logging** – detailed log file with timestamps and statistics
- **Resilient error handling** – validates paths and provides clear feedback

---

![screen0](https://github.com/ZagonAb/RetroPegasus/blob/163a2714e9d185b48b13b2185f07e75759819f28/assets/image/screen0.png)
---
![screen1](https://github.com/ZagonAb/RetroPegasus/blob/163a2714e9d185b48b13b2185f07e75759819f28/assets/image/screen1.png)

## 📋 Requirements

- **Python 3.6+** (Python 3.10+ recommended for best GUI experience)
- **Tkinter** – usually included with Python; on Linux you may need to install `python3-tk` separately
- A valid **RetroArch** installation containing:
  - `playlists/` folder with `.lpl` files
  - `thumbnails/` folder (optional, for media assets)

No additional packages are required – all code uses only the standard library.

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/ZagonAb/RetroPegasus.git
cd RetroPegasus

# Launch the GUI (default)
python3 main.py

# Or use the CLI mode
python3 main.py --cli
```

> 💡 If you're on Linux and get a `No module named tkinter` error, install it with:
> ```bash
> sudo apt install python3-tk   # Debian/Ubuntu
> sudo dnf install python3-tkinter   # Fedora
> ```

---

## 🖥️ GUI Usage Guide

The GUI guides you step by step through the migration process.

### 1. Select RetroArch Installation
- Click **Auto‑detect** to let the tool find your RetroArch folder, or
- Click **Browse…** to manually choose it.

### 2. Choose Output Folder
- The default is `~/pegasus-frontend` (or your OS equivalent).
- You can browse to any existing folder – the tool will create sub‑folders for each system.
- A hint shows whether the folder exists (content will be overwritten) or will be created.

### 3. Pick Media Handling Mode
- **Use absolute paths** (recommended) – no files are copied; uses RetroArch thumbnails directly.
- **Copy media files** – copies boxarts, snaps, logos, and titlescreens into your Pegasus folder (portable, but slower).
- **Skip media** – no images are referenced; metadata only.

### 4. Select Systems to Migrate
- All detected RetroArch playlists are listed with checkboxes.
- Use **Select all** / **Deselect all** to quickly choose.
- Scroll through the list if you have many systems.

### 5. Start Migration
- Click **Start migration** – a live log shows progress.
- A progress bar indicates activity.
- You can **Cancel** at any time (partial files will remain; you'll be prompted to confirm).

### 6. Completion
- A summary dialog shows how many collections and games were processed.
- The log is automatically saved to `retropegasus.log` in your output folder.
- You can expand/hide the log panel at any time.

### Extra GUI Features
- **Language selector** – switch between English, Spanish, Portuguese, and French.
- **Theme selector** – toggle between Light and Dark themes.

---

## ⌨️ CLI Usage Guide

For those who prefer the terminal, the CLI remains fully functional.

Run with:
```bash
python3 main.py --cli
```

Then follow the interactive prompts:

1. **Choose RetroArch source** – auto‑detect or manual path.
2. **Select output folder** – default or custom.
3. **Choose collections** – enter:
   - `a` or `0` for all
   - comma‑separated numbers (e.g., `1,3,5`)
   - ranges (e.g., `2-4`)
   - combinations (e.g., `1,3-5,7`)
4. **Pick media mode** – `1` (absolute), `2` (copy), or `3` (skip).
5. Sit back while the tool processes everything – colourful ANSI output shows progress.

---

## 🧠 How Core Detection Works

RetroPegasus analyses each playlist and decides the best launch strategy:

- **Single core** – if all games share the same core, it writes a single `launch:` line at the collection level.
- **Multiple cores** – if games use different cores (or override the default), it writes a per‑game `launch:` line for each.
- **Fallback** – if a game has no core defined, it uses `DETECT`, letting RetroArch choose automatically.

This preserves your custom core assignments and avoids unnecessary duplication.

---

## 📁 Generated Folder Structure

### With Absolute Paths (Option 1 – recommended)

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
│       │   └── Super Mario World.png
│       ├── screenshot/
│       │   └── Super Mario World.png
│       ├── logo/
│       │   └── Super Mario World.png
│       └── titlescreen/
│           └── Super Mario World.png
├── megadrive/
│   └── ...
└── gba/
    └── ...
```

---

## 📄 Example metadata.txt

```ini
collection: Nintendo - Super Nintendo Entertainment System
shortname: snes
launch: retroarch -L /path/to/snes_libretro.so {file.path}

game: Super Mario World
file: /path/to/roms/Super Mario World.sfc
assets.boxFront: /path/to/thumbnails/Nintendo - SNES/Named_Boxarts/Super Mario World.png
assets.screenshot: /path/to/thumbnails/Nintendo - SNES/Named_Snaps/Super Mario World.png
assets.logo: /path/to/thumbnails/Nintendo - SNES/Named_Logos/Super Mario World.png
assets.titlescreen: /path/to/thumbnails/Nintendo - SNES/Named_Titles/Super Mario World.png
```

---

## 🎮 Supported Systems

The tool includes a comprehensive mapping of RetroArch system names to Pegasus shortnames, covering over **100 systems**.  
A few examples:

| RetroArch System | Pegasus Shortname |
|------------------|-------------------|
| Nintendo - SNES  | snes              |
| Sega - Mega Drive - Genesis | megadrive |
| Sony - PlayStation | psx |
| Nintendo - NES   | nes               |
| Atari - 2600     | atari2600         |
| MAME             | mame              |
| ... and many more | (full list inside `core.py`) |

If a system is not recognised, it will be skipped and logged.

---

## 📝 Logging

A detailed log file `retropegasus.log` is created in your output folder. It records:

- Timestamped entries
- Each playlist processed
- Core detection decisions
- Game counts per system
- Media copy status (if enabled)
- Any errors or warnings

The log is overwritten each time you run the tool, ensuring a clean start.

---

## 🔧 Troubleshooting

**Tkinter not found**  
- On Linux: install `python3-tk` (or equivalent).
- On Windows/macOS: Tkinter is usually included by default with Python.

**No RetroArch installation found**  
- Use the **Browse…** button to manually select your RetroArch folder.
- Ensure the folder contains `playlists/` and `thumbnails/` subdirectories (even if empty).

**Media files not showing up**  
- Check that your RetroArch thumbnails are stored in the expected folder structure:
  `thumbnails/System Name/Named_Boxarts/Game.png`
- If you choose **absolute paths**, Pegasus will look for those exact paths – make sure they are accessible.

**Migration takes too long**  
- If you have many games and choose **copy media**, the process may take a while. Consider using **absolute paths** for faster performance.

---

## 📜 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIT License © 2026 Gonzalo Abbate (ZagonAb)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software without restriction.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

---

## 💖 Support

I'm a programming enthusiast passionate about free software and the retro gaming community. All my themes and projects are open‑source and freely available. If you find this tool useful, consider supporting its continued development:

[![Support on PayPal](https://img.shields.io/badge/PayPal-0070ba?style=for-the-badge)](https://paypal.me/ZagonAb)
[![Donate using Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/Gonzalo/donate)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-29abe0?style=for-the-badge&logo=ko-fi)](https://ko-fi.com/zagonab)

---

**Happy retro-gaming!** 🕹️
