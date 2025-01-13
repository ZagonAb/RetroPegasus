import os
import platform
import shutil
import time
import json
from tqdm import tqdm
from colorama import init, Fore, Style
import sys
import re

init()

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

def print_banner():
    banner = f"""
    {Fore.CYAN}╔══════════════════════════════════════════════╗
    ║          RetroPegasus Converter Tool         ║
    ║     RetroArch → Pegasus Frontend Migration   ║
    ╚══════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def print_menu():
    menu = f"""
    {Fore.YELLOW}[1]{Style.RESET_ALL} Scan RetroArch installation
    {Fore.YELLOW}[2]{Style.RESET_ALL} Enter custom RetroArch path
    {Fore.YELLOW}[3]{Style.RESET_ALL} Exit
    """
    print(menu)

def get_output_path():
    while True:
        print(f"\n{Fore.YELLOW}Select the location to save Pegasus Frontend data:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[1]{Style.RESET_ALL} Use default location on Linux (~/pegasus-frontend)")
        print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Specify custom path")

        choice = input(f"\n{Fore.YELLOW}Select an option (1-2): {Style.RESET_ALL}")

        if choice == "1":
            output_path = os.path.expanduser("~/pegasus-frontend")
        elif choice == "2":
            base_path = input(f"\n{Fore.YELLOW}Enter the path where you want to create the pegasus-frontend folder: {Style.RESET_ALL}")
            base_path = os.path.expanduser(base_path)

            if not os.path.exists(base_path):
                print(f"{Fore.RED}The path {base_path} does not exist.{Style.RESET_ALL}")
                continue

            output_path = os.path.join(base_path, "pegasus-frontend")
        else:
            print(f"{Fore.RED}Invalid option. Please select 1 or 2.{Style.RESET_ALL}")
            continue

        if os.path.exists(output_path):
            print(f"\n{Fore.YELLOW}An existing pegasus-frontend folder was found in:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{output_path}{Style.RESET_ALL}")
            confirm = input(f"{Fore.YELLOW}Do you want to overwrite your content? (y/n): {Style.RESET_ALL}").lower()

            if confirm != 'y':
                continue

            print(f"\n{Fore.YELLOW}⚠️  Warning: Existing content in {output_path} will be overwritten.{Style.RESET_ALL}")
        else:
            try:
                os.makedirs(output_path)
                print(f"\n{Fore.GREEN}✓ New folder created: {output_path}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error creating folder: {e}{Style.RESET_ALL}")
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

    # Verificar la existencia de las carpetas requeridas
    for folder in required_folders:
        folder_path = os.path.join(path, folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Verificar que las carpetas no estén vacías
            if len(os.listdir(folder_path)) > 0:
                required_folders[folder] = True
            else:
                errors.append(f"The '{folder}' folder is empty")
        else:
            errors.append(f"The '{folder}' folder was not found ")

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
                return path  # Retornamos la ruta sin comillas

        return "retroarch.exe"  # Fallback si no se encuentra ninguna ruta

    elif system == "Darwin":
        return "open -a RetroArch --args"
    else:  # Linux
        if os.path.exists("/usr/bin/retroarch"):
            return "retroarch"
        elif os.path.exists(os.path.expanduser("~/.var/app/org.libretro.RetroArch")):
            return "flatpak run org.libretro.RetroArch"
        elif os.path.exists(os.path.expanduser("~/snap/retroarch")):
            return "snap run retroarch"
    return "retroarch"

def find_retroarch_auto():
    system = platform.system()
    print(f"\n{Fore.CYAN}Operating system detected: {system}{Style.RESET_ALL}")

    paths = get_system_paths()
    print(f"\n{Fore.YELLOW}Looking for RetroArch installations...{Style.RESET_ALL}")

    found_paths = []
    for path in paths:
        if os.path.exists(path):
            found_paths.append(path)
            print(f"{Fore.GREEN}✓ Found RetroArch in: {path}{Style.RESET_ALL}")

    if not found_paths:
        print(f"{Fore.RED}No RetroArch installations found.{Style.RESET_ALL}")
        return None

    if len(found_paths) > 1:
        print(f"\n{Fore.YELLOW}Multiple facilities found. Please select one:{Style.RESET_ALL}")
        for i, path in enumerate(found_paths, 1):
            print(f"{Fore.YELLOW}[{i}]{Style.RESET_ALL} {path}")

        while True:
            try:
                choice = int(input("\nSeleccione una opción (número): "))
                if 1 <= choice <= len(found_paths):
                    return found_paths[choice - 1]
                print(f"{Fore.RED}Invalid option. Please try again..{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

    return found_paths[0]

def get_custom_path():
    while True:
        path = input(f"\n{Fore.YELLOW}Enter the RetroArch installation path: {Style.RESET_ALL}")
        if not os.path.exists(path):
            print(f"{Fore.RED}The path entered does not exist. Please check and try again.{Style.RESET_ALL}")
            continue

        # Verificar que la ruta contenga las carpetas necesarias
        is_valid, errors = verify_retroarch_folders(path)

        if not is_valid:
            print(f"\n{Fore.RED}The path does not contain a valid RetroArch installation:{Style.RESET_ALL}")
            for error in errors:
                print(f"{Fore.RED}• {error}{Style.RESET_ALL}")

            retry = input(f"\n{Fore.YELLOW}Would you like to try another path? (y/n): {Style.RESET_ALL}").lower()
            if retry != 'y':
                return None
            continue

        return path

def find_thumbnails_path(base_path):
    thumbnails_path = os.path.join(base_path, "thumbnails")
    if os.path.exists(thumbnails_path):
        print(f"{Fore.GREEN}'thumbnails' folder found: {thumbnails_path}{Style.RESET_ALL}")
        return thumbnails_path
    return None

def find_playlists_path(base_path):
    playlists_path = os.path.join(base_path, "playlists")
    if os.path.exists(playlists_path) and os.path.isdir(playlists_path):
        if len(os.listdir(playlists_path)) > 0:
            print(f"{Fore.GREEN}'playlists' folder found: {playlists_path}{Style.RESET_ALL}")
            return playlists_path
    return None

def copy_images(src, dest):
    png_files = [f for f in os.listdir(src) if f.endswith(".png")]
    for file in tqdm(png_files, desc=f"Copying images in {os.path.basename(dest)}", unit="imagen", leave=False):
        shutil.copy2(os.path.join(src, file), dest)

def process_thumbnails(thumbnails_path, output_path):
    os.makedirs(output_path, exist_ok=True)

    print(f"\n{Fore.YELLOW}Processing thumbnails...{Style.RESET_ALL}")

    valid_systems = []
    for system_folder in os.listdir(thumbnails_path):
        system_path = os.path.join(thumbnails_path, system_folder)
        if os.path.isdir(system_path):
            shortname = SYSTEM_SHORTNAMES.get(system_folder)
            if not shortname:
                print(f"{Fore.YELLOW}System not recognized: {system_folder}, skipping.{Style.RESET_ALL}")
                continue

            boxarts_path = os.path.join(system_path, "Named_Boxarts")
            snaps_path = os.path.join(system_path, "Named_Snaps")

            if not (os.path.exists(boxarts_path) and os.listdir(boxarts_path)):
                continue
            if not (os.path.exists(snaps_path) and os.listdir(snaps_path)):
                continue

            valid_systems.append((system_folder, shortname, boxarts_path, snaps_path))

    for system_folder, shortname, boxarts_path, snaps_path in tqdm(valid_systems, desc="Processing systems", unit="systems"):
        target_system_path = os.path.join(output_path, shortname, "media")
        os.makedirs(os.path.join(target_system_path, "boxFront"), exist_ok=True)
        os.makedirs(os.path.join(target_system_path, "screenshot"), exist_ok=True)

        copy_images(boxarts_path, os.path.join(target_system_path, "boxFront"))
        copy_images(snaps_path, os.path.join(target_system_path, "screenshot"))

def generate_metadata_files(playlists_path, pegasus_home):
    print(f"\n{Fore.YELLOW}Generating metadata.txt files...{Style.RESET_ALL}")

    launch_cmd = get_launch_command()
    system_type = platform.system()

    for playlist_file in tqdm(os.listdir(playlists_path), desc="Processing playlists", unit="playlist"):
        if not playlist_file.endswith('.lpl'):
            continue

        system_name = playlist_file[:-4]
        shortname = SYSTEM_SHORTNAMES.get(system_name)

        if not shortname:
            print(f"{Fore.YELLOW}System not recognized: {system_name}, skipping.{Style.RESET_ALL}")
            continue

        try:
            with open(os.path.join(playlists_path, playlist_file), 'r', encoding='utf-8') as f:
                playlist_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"{Fore.RED}Error reading playlist {playlist_file}: {e}{Style.RESET_ALL}")
            continue

        if 'items' not in playlist_data:
            continue

        core_path = "DETECT"
        for item in playlist_data['items']:
            if item.get('core_path') and item['core_path'] != "DETECT":
                core_path = item['core_path']
                break

        metadata_content = [
            f"collection: {system_name}",
            f"shortname: {shortname}",
            f"launch: {launch_cmd} -L {core_path} {{file.path}}\n"
        ]

        for item in playlist_data['items']:
            full_path = item.get('path', '')
            rom_path = full_path.split('#')[0] if '#' in full_path else full_path

            # Limpieza y normalización de la ruta según el sistema operativo
            if system_type == "Windows":
                # Eliminar ./ del inicio si existe
                if rom_path.startswith('./'):
                    rom_path = rom_path[2:]

                # Eliminar / del inicio si existe
                if rom_path.startswith('/'):
                    rom_path = rom_path[1:]

                # Asegurar que usamos backslashes en Windows
                rom_path = rom_path.replace('/', '\\')

                # Si la ruta no comienza con letra de unidad (C:\, D:\, etc.)
                if not re.match(r'^[A-Za-z]:\\', rom_path):
                    # Añadir C:\ por defecto si no hay letra de unidad
                    rom_path = 'C:\\' + rom_path
            else:
                # Para Linux/macOS
                if rom_path.startswith('./'):
                    rom_path = rom_path[2:]
                if not rom_path.startswith('/'):
                    rom_path = '/' + rom_path

                # Asegurar que usamos forward slashes en Linux/macOS
                rom_path = rom_path.replace('\\', '/')

            game_name = item.get('label', '')
            if not game_name or not rom_path:
                continue

            metadata_content.extend([
                f"game: {game_name}",
                f"file: {rom_path}",
                f"assets.boxFront: ./media/boxFront/{game_name}.png",
                f"assets.screenshot: ./media/screenshot/{game_name}.png\n"
            ])

        system_path = os.path.join(pegasus_home, shortname)
        os.makedirs(system_path, exist_ok=True)

        metadata_path = os.path.join(system_path, "metadata.txt")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata_content))

        print(f"{Fore.GREEN}Metadata generated for {system_name}{Style.RESET_ALL}")

def main():
    while True:
        print_banner()
        print_menu()

        try:
            choice = input(f"\n{Fore.YELLOW}Select an option (1-3): {Style.RESET_ALL}")

            if choice == "1":
                retroarch_path = find_retroarch_auto()
            elif choice == "2":
                retroarch_path = get_custom_path()
                if retroarch_path is None:
                    print(f"\n{Fore.RED}Operation cancelled by user.{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    continue
            elif choice == "3":
                print(f"\n{Fore.CYAN}¡Thank you for using RetroPegasus Converter Tool!{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid option. Please select 1, 2 or 3.{Style.RESET_ALL}")
                continue

            if not retroarch_path:
                input(f"\n{Fore.RED}Press Enter to continue...{Style.RESET_ALL}")
                continue

            # Buscar las carpetas necesarias en la ruta proporcionada
            thumbnails_path = find_thumbnails_path(retroarch_path)
            if not thumbnails_path:
                print(f"{Fore.RED}The 'thumbnails' folder was not found in the specified path.{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                continue

            playlists_path = find_playlists_path(retroarch_path)
            if not playlists_path:
                print(f"{Fore.RED}The 'playlists' folder could not be found in the specified path.{Style.RESET_ALL}")
                input("\nPress Enter to continue...")
                continue

            output_path = get_output_path()

            process_thumbnails(thumbnails_path, output_path)
            generate_metadata_files(playlists_path, output_path)


            print(f"\n{Fore.GREEN}Conversion completed successfully!{Style.RESET_ALL}")
            input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print(f"\n\n{Fore.CYAN}See you later!{Style.RESET_ALL}")
            sys.exit(0)

if __name__ == "__main__":
    main()
