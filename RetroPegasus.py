import os
import platform
import shutil
import time
import json
import sys
import re
import logging

class Colors:
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'


SYSTEM_SHORTNAMES = {
  "Amstrad - CPC": "amstradcpc",
  "Amstrad - GX4000": "gx4000",
  "Arduboy Inc - Arduboy": "arduboy",
  "Atari - 2600": "atari2600",
  "Atari - 5200": "atari5200",
  "Atari - 7800": "atari7800",
  "Atari - 8-bit": "atari8bit",
  "Atari - Jaguar": "atarijaguar",
  "Atari - Lynx": "atarilynx",
  "Atari - ST": "atarist",
  "Atomiswave": "atomiswave",
  "Bandai - WonderSwan": "wonderswan",
  "Bandai - WonderSwan Color": "wonderswancolor",
  "Cannonball": "cannonball",
  "Casio - Loopy": "loopy",
  "Casio - PV-1000": "pv1000",
  "Cave Story": "cavestory",
  "ChaiLove": "chailove",
  "Coleco - ColecoVision": "colecovision",
  "Commodore - 64": "c64",
  "Commodore - Amiga": "amiga",
  "Commodore - CD32": "amigacd32",
  "Commodore - CDTV": "amigacdtv",
  "Commodore - PET": "pet",
  "Commodore - Plus-4": "plus4",
  "Commodore - VIC-20": "vic20",
  "DOOM": "doom",
  "DOS": "dos",
  "Dinothawr": "dinothawr",
  "Emerson - Arcadia 2001": "arcadia2001",
  "Entex - Adventure Vision": "entex",
  "Epoch - Super Cassette Vision": "scv",
  "FBNeo - Arcade Games": "fbneo",
  "Fairchild - Channel F": "channelf",
  "Flashback": "flashback",
  "Funtech - Super Acan": "superarcan",
  "GCE - Vectrex": "vectrex",
  "GamePark - GP32": "gp32",
  "Handheld Electronic Game": "heg",
  "Hartung - Game Master": "gamemaster",
  "Jump 'n Bump": "jumpnbump",
  "LeapFrog - Leapster Learning Game System": "leapfrog",
  "LowRes NX": "lowresnx",
  "Lutro": "lutro",
  "MAME": "mame",
  "Magnavox - Odyssey2": "odyssey2",
  "Mattel - Intellivision": "intellivision",
  "Microsoft - MSX": "msx",
  "Microsoft - MSX2": "msx2",
  "Microsoft - Xbox": "xbox",
  "Microsoft - Xbox 360": "xbox360",
  "MrBoom": "mrboom",
  "NEC - PC Engine - TurboGrafx 16": "tg16",
  "NEC - PC Engine CD - TurboGrafx-CD": "tgcd",
  "NEC - PC Engine SuperGrafx": "supergrafx",
  "NEC - PC-8001 - PC-8801": "pc8001",
  "NEC - PC-98": "necpc98",
  "NEC - PC-FX": "nepcfx",
  "Nintendo - Family Computer Disk System": "ndisk",
  "Nintendo - Game Boy": "gb",
  "Nintendo - Game Boy Advance": "gba",
  "Nintendo - Game Boy Color": "gbc",
  "Nintendo - GameCube": "gamecube",
  "Nintendo - Nintendo 3DS": "3ds",
  "Nintendo - Nintendo 64": "n64",
  "Nintendo - Nintendo 64DD": "n64dd",
  "Nintendo - Nintendo DS": "nds",
  "Nintendo - Nintendo DSi": "ndsi",
  "Nintendo - Nintendo Entertainment System": "nes",
  "Nintendo - Pokemon Mini": "nmini",
  "Nintendo - Satellaview": "satellaview",
  "Nintendo - Sufami Turbo": "sufami",
  "Nintendo - Super Nintendo Entertainment System": "snes",
  "Nintendo - Virtual Boy": "virtualboy",
  "Nintendo - Wii": "wii",
  "Nintendo - Wii U": "wiiu",
  "Philips - CD-i": "cdimono1",
  "Philips - Videopac+": "videopac",
  "Quake": "quake",
  "Quake II": "quakeii",
  "Quake III": "quakeiii",
  "RCA - Studio II": "studioii",
  "RPG Maker": "rpgmaker",
  "Rick Dangerous": "rick",
  "SNK - Neo Geo": "ngp",
  "SNK - Neo Geo CD": "ngcd",
  "SNK - Neo Geo Pocket": "ngp",
  "SNK - Neo Geo Pocket Color": "ngpc",
  "ScummVM": "scummvm",
  "Sega - 32X": "32x",
  "Sega - Dreamcast": "dreamcast",
  "Sega - Game Gear": "gamegear",
  "Sega - Master System - Mark III": "mastersystem",
  "Sega - Mega Drive - Genesis": "megadrive",
  "Sega - Mega-CD - Sega CD": "segacd",
  "Sega - Naomi": "naomi",
  "Sega - Naomi 2": "naomi2",
  "Sega - PICO": "segapico",
  "Sega - SG-1000": "sg1000",
  "Sega - Saturn": "saturn",
  "Sharp - X1": "sharpx1",
  "Sharp - X68000": "x68000",
  "Sinclair - ZX 81": "sinclair",
  "Sinclair - ZX Spectrum": "spectrum",
  "Sony - PlayStation": "psx",
  "Sony - PlayStation 2": "ps2",
  "Sony - PlayStation 3": "ps3",
  "Sony - PlayStation 4": "ps4",
  "Sony - PlayStation Portable": "psp",
  "Sony - PlayStation Vita": "vita",
  "Spectravideo - SVI-318 - SVI-328": "spectravideo",
  "TIC-80": "tic80",
  "The 3DO Company - 3DO": "3do",
  "Thomson - MOTO": "thomson",
  "Tiger - Game.com": "gamecom",
  "Tomb Raider": "tombraider",
  "VTech - CreatiVision": "creatiVision",
  "VTech - V.Smile": "vsmile",
  "Vircon32": "vircon32",
  "WASM-4": "wasm4",
  "Watara - Supervision": "watara",
  "Wolfenstein 3D": "wolfenstein"
}

MEDIA_MAPPING = {
    "Named_Boxarts": "boxFront",
    "Named_Snaps": "screenshot",
    "Named_Logos": "logo",
    "Named_Titles": "titlescreen"
}


def detect_core_mode(playlist_data, logger, system_name):
    items = playlist_data.get('items', [])
    if not items:
        return None, False

    cores = set()
    for item in items:
        core = item.get('core_path', '').strip()
        if core and core != 'DETECT':
            cores.add(core)

    default_core = playlist_data.get('default_core_path', '').strip()
    if default_core and default_core != 'DETECT':
        cores.add(default_core)

    if not cores:
        logger.info(f"{system_name}: No cores found. Using global DETECT.")
        return 'DETECT', False
    if len(cores) == 1:
        global_core = cores.pop()
        logger.info(f"{system_name}: All games share the same core: {global_core}")
        return global_core, False
    else:
        logger.info(f"{system_name}: Multiple cores detected ({', '.join(cores)}). Using per‑game launch.")
        return None, True


def print_banner():
    banner = f"""
    {Colors.CYAN}╔══════════════════════════════════════════════╗
    ║          RetroPegasus Converter Tool         ║
    ║     RetroArch → Pegasus Frontend Migration   ║
    ╚══════════════════════════════════════════════╝{Colors.RESET}
    """
    print(banner)


def print_menu():
    menu = f"""
    {Colors.YELLOW}[1]{Colors.RESET} Scan RetroArch installation
    {Colors.YELLOW}[2]{Colors.RESET} Enter custom RetroArch path
    {Colors.YELLOW}[3]{Colors.RESET} Exit
    """
    print(menu)


def setup_logging(output_path):
    log_file = os.path.join(output_path, "retropegasus.log")

    logger = logging.getLogger()
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    return logger


def get_output_path():
    while True:
        print(f"\n{Colors.YELLOW}Select the location to save Pegasus Frontend data:{Colors.RESET}")
        print(f"{Colors.YELLOW}[1]{Colors.RESET} Use default location on Linux (~/pegasus-frontend)")
        print(f"{Colors.YELLOW}[2]{Colors.RESET} Specify custom path")

        choice = input(f"\n{Colors.YELLOW}Select an option (1-2): {Colors.RESET}")

        if choice == "1":
            output_path = os.path.expanduser("~/pegasus-frontend")
        elif choice == "2":
            base_path = input(f"\n{Colors.YELLOW}Enter the path where you want to create the pegasus-frontend folder: {Colors.RESET}")
            base_path = os.path.expanduser(base_path)

            if not os.path.exists(base_path):
                print(f"{Colors.RED}The path {base_path} does not exist.{Colors.RESET}")
                continue

            output_path = os.path.join(base_path, "pegasus-frontend")
        else:
            print(f"{Colors.RED}Invalid option. Please select 1 or 2.{Colors.RESET}")
            continue

        if os.path.exists(output_path):
            print(f"\n{Colors.YELLOW}An existing pegasus-frontend folder was found at:{Colors.RESET}")
            print(f"{Colors.YELLOW}{output_path}{Colors.RESET}")
            confirm = input(f"{Colors.YELLOW}Do you want to overwrite its content? (y/n): {Colors.RESET}").lower()

            if confirm != 'y':
                continue

            print(f"\n{Colors.YELLOW}⚠️  Warning: Existing content in {output_path} will be overwritten.{Colors.RESET}")
        else:
            try:
                os.makedirs(output_path)
                print(f"\n{Colors.GREEN}✓ New folder created: {output_path}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}Error creating folder: {e}{Colors.RESET}")
                continue

        return output_path


def get_system_paths():
    system = platform.system()
    if system == "Windows":
        return [
            os.path.join(os.getenv('APPDATA'), "RetroArch"),
            "C:\\Program Files\\RetroArch",
            "C:\\Program Files (x86)\\RetroArch",
            "C:\\RetroArch-Win64",
            "C:\\RetroArch-Win32"
        ]
    elif system == "Linux":
        return [
            "/usr/bin/retroarch",
            os.path.expanduser("~/.var/app/org.libretro.RetroArch/config/retroarch/"),
            os.path.expanduser("~/snap/retroarch/current/retroarch"),
            os.path.expanduser("~/.config/retroarch")
        ]
    elif system == "Darwin":
        return [
            os.path.expanduser("~/Library/Application Support/RetroArch"),
            "/Applications/RetroArch.app",
            os.path.expanduser("~/Applications/RetroArch.app")
        ]
    return []


def verify_retroarch_folders(path):
    required_folders = {
        'thumbnails': False,
        'playlists': False
    }

    errors = []

    for folder in required_folders:
        folder_path = os.path.join(path, folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            if len(os.listdir(folder_path)) > 0:
                required_folders[folder] = True
            else:
                errors.append(f"The '{folder}' folder is empty")
        else:
            errors.append(f"The '{folder}' folder was not found")

    all_valid = all(required_folders.values())

    return all_valid, errors


def get_launch_command():
    system = platform.system()
    if system == "Windows":
        possible_paths = [
            os.path.join(os.getenv('PROGRAMFILES'), "RetroArch", "retroarch.exe"),
            os.path.join(os.getenv('PROGRAMFILES(X86)'), "RetroArch", "retroarch.exe"),
            os.path.join(os.getenv('APPDATA'), "RetroArch", "retroarch.exe"),
            os.path.join(os.getenv('LOCALAPPDATA'), "RetroArch", "retroarch.exe"),
            "C:\\RetroArch-Win64\\retroarch.exe",
            "C:\\RetroArch-Win32\\retroarch.exe"
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        return "retroarch.exe"

    elif system == "Darwin":
        return "open -a RetroArch --args"
    else:
        if os.path.exists("/usr/bin/retroarch"):
            return "retroarch"
        elif os.path.exists(os.path.expanduser("~/.var/app/org.libretro.RetroArch")):
            return "flatpak run org.libretro.RetroArch"
        elif os.path.exists(os.path.expanduser("~/snap/retroarch")):
            return "snap run retroarch"
    return "retroarch"


def find_retroarch_auto():
    system = platform.system()
    print(f"\n{Colors.CYAN}Operating system detected: {system}{Colors.RESET}")

    paths = get_system_paths()
    print(f"\n{Colors.YELLOW}Looking for RetroArch installations...{Colors.RESET}")

    found_paths = []
    for path in paths:
        if os.path.exists(path):
            found_paths.append(path)
            print(f"{Colors.GREEN}✓ Found RetroArch at: {path}{Colors.RESET}")

    if not found_paths:
        print(f"{Colors.RED}No RetroArch installations found.{Colors.RESET}")
        return None

    if len(found_paths) > 1:
        print(f"\n{Colors.YELLOW}Multiple installations found. Please select one:{Colors.RESET}")
        for i, path in enumerate(found_paths, 1):
            print(f"{Colors.YELLOW}[{i}]{Colors.RESET} {path}")

        while True:
            try:
                choice = int(input("\nSelect an option (number): "))
                if 1 <= choice <= len(found_paths):
                    return found_paths[choice - 1]
                print(f"{Colors.RED}Invalid option. Please try again.{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}Please enter a valid number.{Colors.RESET}")

    return found_paths[0]


def get_custom_path():
    while True:
        path = input(f"\n{Colors.YELLOW}Enter the RetroArch installation path: {Colors.RESET}")
        if not os.path.exists(path):
            print(f"{Colors.RED}The path does not exist. Please check and try again.{Colors.RESET}")
            continue

        is_valid, errors = verify_retroarch_folders(path)

        if not is_valid:
            print(f"\n{Colors.RED}The path does not contain a valid RetroArch installation:{Colors.RESET}")
            for error in errors:
                print(f"{Colors.RED}• {error}{Colors.RESET}")

            retry = input(f"\n{Colors.YELLOW}Would you like to try another path? (y/n): {Colors.RESET}").lower()
            if retry != 'y':
                return None
            continue

        return path


def find_thumbnails_path(base_path):
    thumbnails_path = os.path.join(base_path, "thumbnails")
    if os.path.exists(thumbnails_path):
        print(f"{Colors.GREEN}'thumbnails' folder found at: {thumbnails_path}{Colors.RESET}")
        return thumbnails_path
    return None


def find_playlists_path(base_path):
    playlists_path = os.path.join(base_path, "playlists")
    if os.path.exists(playlists_path) and os.path.isdir(playlists_path):
        if len(os.listdir(playlists_path)) > 0:
            print(f"{Colors.GREEN}'playlists' folder found at: {playlists_path}{Colors.RESET}")
            return playlists_path
    return None


def get_media_handling_mode():
    while True:
        print(f"\n{Colors.YELLOW}How do you want to handle media files (images)?{Colors.RESET}")
        print(f"{Colors.YELLOW}[1]{Colors.RESET} Use absolute paths (recommended) - No files copied, uses RetroArch thumbnails directly")
        print(f"{Colors.YELLOW}[2]{Colors.RESET} Copy images to Pegasus folder")
        print(f"{Colors.YELLOW}[3]{Colors.RESET} Skip media files entirely (only generate metadata.txt)")

        choice = input(f"\n{Colors.YELLOW}Select an option (1-3): {Colors.RESET}")

        if choice in ['1', '2', '3']:
            return choice
        print(f"{Colors.RED}Invalid option. Please select 1, 2 or 3.{Colors.RESET}")


def select_playlists(playlists_path):
    playlist_files = [f for f in os.listdir(playlists_path) if f.endswith('.lpl')]
    if not playlist_files:
        print(f"{Colors.RED}No playlist files found.{Colors.RESET}")
        return []

    playlist_files.sort()

    print(f"\n{Colors.YELLOW}Available collections (playlists):{Colors.RESET}")
    for idx, filename in enumerate(playlist_files, 1):
        system_name = filename[:-4]
        shortname = SYSTEM_SHORTNAMES.get(system_name, "unknown")
        print(f"  {Colors.YELLOW}[{idx}]{Colors.RESET} {system_name} ({shortname})")

    print(f"\n{Colors.CYAN}Enter the numbers of the collections to process.{Colors.RESET}")
    print(f"  {Colors.CYAN}Examples:{Colors.RESET}")
    print(f"    • 'a' or '0'  → process all")
    print(f"    • '1,3,5'     → process collections 1, 3, and 5")
    print(f"    • '2-4'       → process collections 2, 3, and 4")
    print(f"    • '1,3-5,7'   → process 1, 3, 4, 5, and 7")

    while True:
        choice = input(f"\n{Colors.YELLOW}Your selection: {Colors.RESET}").strip()

        if choice.lower() in ('a', '0'):
            return [f[:-4] for f in playlist_files]

        selected_indices = set()
        parts = choice.split(',')
        valid = True
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = part.split('-')
                    start = int(start.strip())
                    end = int(end.strip())
                    if start < 1 or end > len(playlist_files) or start > end:
                        print(f"{Colors.RED}Invalid range: {part}. Please try again.{Colors.RESET}")
                        valid = False
                        break
                    for i in range(start, end + 1):
                        selected_indices.add(i)
                except ValueError:
                    print(f"{Colors.RED}Invalid range: {part}. Please try again.{Colors.RESET}")
                    valid = False
                    break
            else:
                try:
                    num = int(part)
                    if num < 1 or num > len(playlist_files):
                        print(f"{Colors.RED}Number {num} is out of range (1-{len(playlist_files)}). Please try again.{Colors.RESET}")
                        valid = False
                        break
                    selected_indices.add(num)
                except ValueError:
                    print(f"{Colors.RED}Invalid input: {part}. Please try again.{Colors.RESET}")
                    valid = False
                    break

        if not valid:
            continue

        if not selected_indices:
            print(f"{Colors.RED}No valid selections made. Please try again.{Colors.RESET}")
            continue

        selected_systems = []
        for idx in sorted(selected_indices):
            filename = playlist_files[idx - 1]
            system_name = filename[:-4]
            selected_systems.append(system_name)

        return selected_systems


def generate_metadata_absolute(playlists_path, pegasus_home, thumbnails_base_path, logger, selected_systems=None):
    logger.info("=== Generating metadata.txt files with absolute media paths ===")
    print(f"\n{Colors.YELLOW}Generating metadata.txt with absolute media paths...{Colors.RESET}")

    launch_cmd_base = get_launch_command()
    system_type = platform.system()

    all_playlist_files = [f for f in os.listdir(playlists_path) if f.endswith('.lpl')]

    if selected_systems is not None:
        playlist_files = [f for f in all_playlist_files if f[:-4] in selected_systems]
    else:
        playlist_files = all_playlist_files

    total_playlists = len(playlist_files)
    logger.info(f"Found {total_playlists} playlist files to process (out of {len(all_playlist_files)} total)")

    print(f"{Colors.CYAN}Processing {total_playlists} playlist files{Colors.RESET}\n")

    processed = 0
    total_games = 0

    for idx, playlist_file in enumerate(playlist_files, 1):
        system_name = playlist_file[:-4]
        print(f"{Colors.YELLOW}[{idx}/{total_playlists}] Processing: {system_name}{Colors.RESET}")
        logger.info(f"--- Processing playlist: {system_name} ---")

        shortname = SYSTEM_SHORTNAMES.get(system_name)
        if not shortname:
            msg = f"System not recognized: {system_name}, skipping."
            logger.warning(msg)
            print(f"{Colors.YELLOW}  {msg}{Colors.RESET}")
            continue

        try:
            with open(os.path.join(playlists_path, playlist_file), 'r', encoding='utf-8') as f:
                playlist_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error reading playlist {playlist_file}: {e}")
            print(f"{Colors.RED}  Error reading playlist: {e}{Colors.RESET}")
            continue

        if 'items' not in playlist_data or not playlist_data['items']:
            logger.warning(f"No items in {playlist_file}")
            print(f"{Colors.YELLOW}  No games found in this playlist, skipping.{Colors.RESET}")
            continue

        global_core, use_individual = detect_core_mode(playlist_data, logger, system_name)

        metadata_content = [
            f"collection: {system_name}",
            f"shortname: {shortname}"
        ]

        if not use_individual:
            metadata_content.append(f"launch: {launch_cmd_base} -L {global_core} {{file.path}}")
        metadata_content.append("")

        games_count = 0
        for item in playlist_data['items']:
            full_path = item.get('path', '')
            rom_path = full_path.split('#')[0] if '#' in full_path else full_path

            if system_type == "Windows":
                if rom_path.startswith('./'):
                    rom_path = rom_path[2:]
                if rom_path.startswith('/'):
                    rom_path = rom_path[1:]
                rom_path = rom_path.replace('/', '\\')
                if not re.match(r'^[A-Za-z]:\\', rom_path):
                    rom_path = 'C:\\' + rom_path
            else:
                if rom_path.startswith('./'):
                    rom_path = rom_path[2:]
                if not rom_path.startswith('/'):
                    rom_path = '/' + rom_path
                rom_path = rom_path.replace('\\', '/')

            game_name = item.get('label', '')
            if not game_name or not rom_path:
                continue

            games_count += 1
            total_games += 1

            game_metadata = [f"game: {game_name}", f"file: {rom_path}"]

            if use_individual:
                core_for_game = item.get('core_path', '').strip()
                if not core_for_game or core_for_game == 'DETECT':
                    default_core = playlist_data.get('default_core_path', '').strip()
                    if default_core and default_core != 'DETECT':
                        core_for_game = default_core
                        logger.info(f"Game '{game_name}' has no core, using default_core_path: {default_core}")
                    else:
                        core_for_game = 'DETECT'
                        logger.warning(f"Game '{game_name}' has no core defined, using DETECT")
                game_metadata.append(f"launch: {launch_cmd_base} -L {core_for_game} {{file.path}}")

            for retroarch_media, pegasus_media in MEDIA_MAPPING.items():
                media_file_path = os.path.join(thumbnails_base_path, system_name, retroarch_media, f"{game_name}.png")
                if os.path.exists(media_file_path):
                    game_metadata.append(f"assets.{pegasus_media}: {media_file_path}")

            game_metadata.append("")
            metadata_content.extend(game_metadata)

        system_path = os.path.join(pegasus_home, shortname)
        os.makedirs(system_path, exist_ok=True)

        metadata_path = os.path.join(system_path, "metadata.txt")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata_content))

        processed += 1
        if not use_individual:
            logger.info(f"Generated {system_name} with {games_count} games (global core: {global_core})")
            print(f"{Colors.GREEN}  ✓ Generated {system_name} with {games_count} games (global core){Colors.RESET}")
            print(f"  {Colors.CYAN}  Core used: {global_core}{Colors.RESET}")
        else:
            logger.info(f"Generated {system_name} with {games_count} games (per‑game cores)")
            print(f"{Colors.GREEN}  ✓ Generated {system_name} with {games_count} games (per‑game cores){Colors.RESET}")
        print("")

    logger.info(f"=== Finished processing {processed} playlists, total games: {total_games} ===")
    return processed, total_games


def generate_metadata_no_media(playlists_path, pegasus_home, logger, selected_systems=None):
    logger.info("=== Generating metadata.txt files without media ===")
    print(f"\n{Colors.YELLOW}Generating metadata.txt without media...{Colors.RESET}")

    launch_cmd_base = get_launch_command()
    system_type = platform.system()

    all_playlist_files = [f for f in os.listdir(playlists_path) if f.endswith('.lpl')]

    if selected_systems is not None:
        playlist_files = [f for f in all_playlist_files if f[:-4] in selected_systems]
    else:
        playlist_files = all_playlist_files

    total_playlists = len(playlist_files)
    logger.info(f"Found {total_playlists} playlist files to process (out of {len(all_playlist_files)} total)")

    print(f"{Colors.CYAN}Processing {total_playlists} playlist files{Colors.RESET}\n")

    processed = 0
    total_games = 0

    for idx, playlist_file in enumerate(playlist_files, 1):
        system_name = playlist_file[:-4]
        print(f"{Colors.YELLOW}[{idx}/{total_playlists}] Processing: {system_name}{Colors.RESET}")
        logger.info(f"--- Processing playlist: {system_name} ---")

        shortname = SYSTEM_SHORTNAMES.get(system_name)
        if not shortname:
            msg = f"System not recognized: {system_name}, skipping."
            logger.warning(msg)
            print(f"{Colors.YELLOW}  {msg}{Colors.RESET}")
            continue

        try:
            with open(os.path.join(playlists_path, playlist_file), 'r', encoding='utf-8') as f:
                playlist_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error reading playlist {playlist_file}: {e}")
            print(f"{Colors.RED}  Error reading playlist: {e}{Colors.RESET}")
            continue

        if 'items' not in playlist_data or not playlist_data['items']:
            logger.warning(f"No items in {playlist_file}")
            print(f"{Colors.YELLOW}  No games found in this playlist, skipping.{Colors.RESET}")
            continue

        global_core, use_individual = detect_core_mode(playlist_data, logger, system_name)

        metadata_content = [
            f"collection: {system_name}",
            f"shortname: {shortname}"
        ]

        if not use_individual:
            metadata_content.append(f"launch: {launch_cmd_base} -L {global_core} {{file.path}}")
        metadata_content.append("")

        games_count = 0
        for item in playlist_data['items']:
            full_path = item.get('path', '')
            rom_path = full_path.split('#')[0] if '#' in full_path else full_path

            if system_type == "Windows":
                if rom_path.startswith('./'):
                    rom_path = rom_path[2:]
                if rom_path.startswith('/'):
                    rom_path = rom_path[1:]
                rom_path = rom_path.replace('/', '\\')
                if not re.match(r'^[A-Za-z]:\\', rom_path):
                    rom_path = 'C:\\' + rom_path
            else:
                if rom_path.startswith('./'):
                    rom_path = rom_path[2:]
                if not rom_path.startswith('/'):
                    rom_path = '/' + rom_path
                rom_path = rom_path.replace('\\', '/')

            game_name = item.get('label', '')
            if not game_name or not rom_path:
                continue

            games_count += 1
            total_games += 1

            game_metadata = [f"game: {game_name}", f"file: {rom_path}"]

            if use_individual:
                core_for_game = item.get('core_path', '').strip()
                if not core_for_game or core_for_game == 'DETECT':
                    default_core = playlist_data.get('default_core_path', '').strip()
                    if default_core and default_core != 'DETECT':
                        core_for_game = default_core
                        logger.info(f"Game '{game_name}' has no core, using default_core_path: {default_core}")
                    else:
                        core_for_game = 'DETECT'
                        logger.warning(f"Game '{game_name}' has no core defined, using DETECT")
                game_metadata.append(f"launch: {launch_cmd_base} -L {core_for_game} {{file.path}}")

            game_metadata.append("")
            metadata_content.extend(game_metadata)

        system_path = os.path.join(pegasus_home, shortname)
        os.makedirs(system_path, exist_ok=True)

        metadata_path = os.path.join(system_path, "metadata.txt")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata_content))

        processed += 1
        if not use_individual:
            logger.info(f"Generated {system_name} with {games_count} games (global core: {global_core})")
            print(f"{Colors.GREEN}  ✓ Generated {system_name} with {games_count} games (global core){Colors.RESET}")
            print(f"  {Colors.CYAN}  Core used: {global_core}{Colors.RESET}")
        else:
            logger.info(f"Generated {system_name} with {games_count} games (per‑game cores)")
            print(f"{Colors.GREEN}  ✓ Generated {system_name} with {games_count} games (per‑game cores){Colors.RESET}")
        print("")

    logger.info(f"=== Finished processing {processed} playlists, total games: {total_games} ===")
    return processed, total_games


def main():
    logger = None
    total_playlists = 0
    total_games = 0

    while True:
        print_banner()
        print_menu()

        try:
            choice = input(f"\n{Colors.YELLOW}Select an option (1-3): {Colors.RESET}")

            if choice == "1":
                retroarch_path = find_retroarch_auto()
            elif choice == "2":
                retroarch_path = get_custom_path()
                if retroarch_path is None:
                    print(f"\n{Colors.RED}Operation cancelled by user.{Colors.RESET}")
                    input("\nPress Enter to continue...")
                    continue
            elif choice == "3":
                print(f"\n{Colors.CYAN}Thank you for using RetroPegasus Converter Tool!{Colors.RESET}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Invalid option. Please select 1, 2 or 3.{Colors.RESET}")
                continue

            if not retroarch_path:
                input(f"\n{Colors.RED}Press Enter to continue...{Colors.RESET}")
                continue

            thumbnails_path = find_thumbnails_path(retroarch_path)
            if not thumbnails_path:
                print(f"{Colors.RED}The 'thumbnails' folder was not found at the specified path.{Colors.RESET}")
                input("\nPress Enter to continue...")
                continue

            playlists_path = find_playlists_path(retroarch_path)
            if not playlists_path:
                print(f"{Colors.RED}The 'playlists' folder was not found at the specified path.{Colors.RESET}")
                input("\nPress Enter to continue...")
                continue

            output_path = get_output_path()

            logger = setup_logging(output_path)
            logger.info("=== RetroPegasus Converter Tool Started ===")
            logger.info(f"Output path: {output_path}")
            logger.info(f"RetroArch path: {retroarch_path}")
            logger.info(f"Thumbnails path: {thumbnails_path}")
            logger.info(f"Playlists path: {playlists_path}")
            selected_systems = select_playlists(playlists_path)
            if not selected_systems:
                print(f"{Colors.RED}No collections selected. Aborting.{Colors.RESET}")
                input("\nPress Enter to continue...")
                continue

            logger.info(f"Selected collections: {', '.join(selected_systems)}")

            media_mode = get_media_handling_mode()
            logger.info(f"Media handling mode: {media_mode}")

            if media_mode == '1':
                print(f"\n{Colors.CYAN}Using absolute paths for media (recommended){Colors.RESET}")
                processed, games = generate_metadata_absolute(
                    playlists_path, output_path, thumbnails_path, logger, selected_systems
                )
            elif media_mode == '2':
                print(f"\n{Colors.CYAN}Copying media files...{Colors.RESET}")
                logger.warning("Mode 2 (copy media) is not implemented. Falling back to mode 1.")
                print(f"{Colors.YELLOW}⚠️  Copy mode not implemented. Using mode 1 as fallback.{Colors.RESET}")
                processed, games = generate_metadata_absolute(
                    playlists_path, output_path, thumbnails_path, logger, selected_systems
                )
            else:
                print(f"\n{Colors.CYAN}Skipping media files...{Colors.RESET}")
                processed, games = generate_metadata_no_media(
                    playlists_path, output_path, logger, selected_systems
                )

            total_playlists += processed
            total_games += games

            logger.info("=== Conversion completed successfully ===")
            logger.info(f"Total playlists processed: {total_playlists}")
            logger.info(f"Total games: {total_games}")

            print(f"\n{Colors.GREEN}✓ Conversion completed successfully!{Colors.RESET}")
            print(f"{Colors.CYAN}Total playlists processed: {total_playlists}{Colors.RESET}")
            print(f"{Colors.CYAN}Total games: {total_games}{Colors.RESET}")
            input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}See you later!{Colors.RESET}")
            if logger:
                logger.info("Process interrupted by user.")
            sys.exit(0)


if __name__ == "__main__":
    main()
