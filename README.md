# RetroPegasus Converter Tool

RetroPegasus is a command-line tool that makes it easy to migrate your RetroArch library to Pegasus Frontend by automating metadata creation and asset organization.

## 🚀 Characteristics

- Automatic detection of RetroArch installations on Windows, Linux and macOS
- Support for custom installation paths
- Automatic migration of images (boxarts and screenshots)
- Automatic generation of metadata.txt files compatible with Pegasus Frontend
- Colored command line interface for better readability
- Progress bar for long operations
- Error handling and path validation

## 📋 Prerequisites

### Python Dependencies
```
colorama
tqdm
```

### Installing Dependencies
```bash
pip install colorama tqdm
```

## 💻 Supported Operating Systems

### Windows
- Supported automatic routes:
  - %APPDATA%/RetroArch
  - C:\Program Files\RetroArch
  - C:\Program Files (x86)\RetroArch
  - C:\\RetroArch-Win32
  - C:\\RetroArch-Win64

### Linux
- Supported automatic routes:
  - /usr/bin/retroarch
  - ~/.var/app/org.libretro.RetroArch/config/retroarch/
  - ~/snap/retroarch/current/retroarch
  - ~/.config/retroarch

### macOS
- Supported automatic routes:
  - ~/Library/Application Support/RetroArch
  - /Applications/RetroArch.app

<details>
  <summary>🎮 Supported Game Systems</summary>

  - Amstrad - CPC = amstradcpc
  - Amstrad - GX4000 = gx4000
  - Arduboy Inc - Arduboy = arduboy
  - Atari - 2600 = atari2600
  - Atari - 5200 = atari5200
  - Atari - 7800 = atari7800
  - Atari - 8-bit = atari8bit
  - Atari - Jaguar = atarijaguar
  - Atari - Lynx = atarilynx
  - Atari - ST = atarist
  - Atomiswave = atomiswave
  - Bandai - WonderSwan = wonderswan
  - Bandai - WonderSwan Color = wonderswancolor
  - Cannonball = cannonball
  - Casio - Loopy = loopy
  - Casio - PV-1000 = pv1000
  - Cave Story = cavestory
  - ChaiLove = chailove
  - Coleco - ColecoVision = colecovision
  - Commodore - 64 = c64
  - Commodore - Amiga = amiga
  - Commodore - CD32 = amigacd32
  - Commodore - CDTV = amigacdtv
  - Commodore - PET = pet
  - Commodore - Plus-4 = plus
  - Commodore - VIC-20 = vic20
  - DOOM = doom
  - DOS = dos
  - Dinothawr = dinothawr
  - Emerson - Arcadia 2001 = arcadia2001
  - Entex - Adventure Vision = entex
  - Epoch - Super Cassette Vision = scv
  - FBNeo - Arcade Games = fbneo
  - Fairchild - Channel F = channelf
  - Flashback = flashback
  - Funtech - Super Acan = superarcan
  - GCE - Vectrex = vectrex
  - GamePark - GP32 = gp32
  - Handheld Electronic Game = heg
  - Hartung - Game Master = gamemaster
  - Jump 'n Bump = jumpnbump
  - LeapFrog - Leapster Learning Game System = leapfrog
  - LowRes NX = lowresnx
  - Lutro = lutro
  - MAME = mame
  - Magnavox - Odyssey2 = odyssey2
  - Mattel - Intellivision = intellivision
  - Microsoft - MSX = msx
  - Microsoft - MSX2 = msx2
  - Microsoft - Xbox = xbox
  - Microsoft - Xbox 360 = xbox360
  - MrBoom = mrboom
  - NEC - PC Engine - TurboGrafx 16 = tg16
  - NEC - PC Engine CD - TurboGrafx-CD = tgcd
  - NEC - PC Engine SuperGrafx = supergrafx
  - NEC - PC-8001 - PC-8801 = pc8001
  - NEC - PC-98 = necpc98
  - NEC - PC-FX = nepcfx
  - Nintendo - Family Computer Disk System = ndisk
  - Nintendo - Game Boy = gb
  - Nintendo - Game Boy Advance = gba
  - Nintendo - Game Boy Color = gbc
  - Nintendo - GameCube = gamecube
  - Nintendo - Nintendo 3DS = 3ds
  - Nintendo - Nintendo 64 = n64
  - Nintendo - Nintendo 64DD = n64dd
  - Nintendo - Nintendo DS = nds
  - Nintendo - Nintendo DSi = ndsi
  - Nintendo - Nintendo Entertainment System = nes
  - Nintendo - Pokemon Mini = nmini
  - Nintendo - Satellaview = satellaview
  - Nintendo - Sufami Turbo = sufami
  - Nintendo - Super Nintendo Entertainment System = snes
  - Nintendo - Virtual Boy = virtualboy
  - Nintendo - Wii = wii
  - Nintendo - Wii U = wiiu
  - Philips - CD-i = cdimono1
  - Philips - Videopac+ = videopac
  - Quake = quake
  - Quake II = quakeii
  - Quake III = quakeiii
  - RCA - Studio II = studioii
  - RPG Maker = rpgmaker
  - Rick Dangerous = rick
  - SNK - Neo Geo = ngp
  - SNK - Neo Geo CD = ngcd
  - SNK - Neo Geo Pocket = ngp
  - SNK - Neo Geo Pocket Color = ngpc
  - ScummVM = scummvm
  - Sega - 32X = 32x
  - Sega - Dreamcast = dreamcast
  - Sega - Game Gear = gamegear
  - Sega - Master System - Mark III = mastersystem
  - Sega - Mega Drive - Genesis = megadrive
  - Sega - Mega-CD - Sega CD = segacd
  - Sega - Naomi = naomi
  - Sega - Naomi 2 = naomi2
  - Sega - PICO = segapico
  - Sega - SG-1000 = sg1000
  - Sega - Saturn = saturn
  - Sharp - X1 = sharpx1
  - Sharp - X68000 = x68000
  - Sinclair - ZX 81 = sinclair
  - Sinclair - ZX Spectrum = spectrum
  - Sony - PlayStation = psx
  - Sony - PlayStation 2 = ps2
  - Sony - PlayStation 3 = ps3
  - Sony - PlayStation 4 = ps4
  - Sony - PlayStation Portable = psp
  - Sony - PlayStation Vita = vita
  - Spectravideo - SVI-318 - SVI-328 = spectravideo
  - TIC-80 = tic80
  - The 3DO Company - 3DO = 3do
  - Thomson - MOTO = thomson
  - Tiger - Game.com = gamecom
  - Tomb Raider = tombraider
  - VTech - CreatiVision = creatiVision
  - VTech - V.Smile = vsmile
  - Vircon32 = vircon32
  - WASM-4 = wasm4
  - Watara - Supervision = watara
  - Wolfenstein 3D = wolfenstein
  
</details>

## 📁 Generated File Structure

```
~/pegasus-frontend/
├── [system]/
│   ├── metadata.txt
│   └── media/
│       ├── boxFront/
│       │   └── [images of boxes]
│       └── screenshot/
│           └── [screenshots]
```

## 🛠️ Use

1. Run the script:
```bash
python retropegasus.py
```

2. Select an option:
   - `1`: RetroArch Automatic Installation Scan
   - `2`: Enter custom path
   - `3`: Exit

3. The script:
   - It will search for the necessary folders (thumbnails and playlists)
   - It will process the thumbnails and copy them to the Pegasus structure
   - It will generate the necessary metadata.txt files

## 📄 Generated Files

### metadata.txt
Contains the information needed by Pegasus Frontend:
- Collection name
- Launch command
- List of games with their paths and assets
- Paths to images (boxart and screenshots)

## ⚠️ RetroArch Requirements
Your RetroArch installation should have:
1. `thumbnails` folder with:
- Named_Boxarts
- Named_Snaps
2. `playlists` folder with .lpl files

## 🔍 Validation

The script checks:
- Existence of RetroArch installation
- Presence of required folders
- Valid content in folders
- Correct file formats

## 🤝 Contribution

If you find bugs or have improvements to suggest:
1. Open an issue
2. Describe the problem or improvement
3. If possible, provide examples

## 📝 Remember

- Game paths in metadata.txt are absolute
- Asset paths are relative to the system folder
- The script preserves the original structure of RetroArch playlists

## 📜 License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Licencia Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"></a>
