import os
import shutil
import time
import json
from tqdm import tqdm

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
  "LeapFrog - Leapster Learning Game System": "",
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

def find_retroarch():
    paths = [
        "/usr/bin/retroarch",  # Instalado con apt
        os.path.expanduser("~/.var/app/org.libretro.RetroArch/config/retroarch/"),  # Flatpak
        os.path.expanduser("~/snap/retroarch/current/retroarch"),  # Snap
        os.path.expanduser("~/.config/retroarch") #apt

    ]

    for path in paths:
        if os.path.exists(path):
            print(f"RetroArch encontrado: {path}")
            return os.path.dirname(path)
    return None

def find_thumbnails_path(base_path):
    possible_paths = [
        os.path.expanduser("~/.config/retroarch/thumbnails"),  # Ruta estándar para apt
        os.path.expanduser("~/.var/app/org.libretro.RetroArch/config/retroarch/thumbnails"),  # Flatpak
        os.path.expanduser("~/snap/retroarch/current/.config/retroarch/thumbnails")  # Snap
    ]

    for path in possible_paths:
        if os.path.exists(path):
            print(f"Carpeta 'thumbnails' encontrada: {path}")
            return path
    return None

def find_playlists_path():
    possible_paths = [
        os.path.expanduser("~/.config/retroarch/playlists"),  # Ruta estándar para apt
        os.path.expanduser("~/.var/app/org.libretro.RetroArch/config/retroarch/playlists"),  # Flatpak
        os.path.expanduser("~/snap/retroarch/current/.config/retroarch/playlists")  # Snap
    ]

    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            if len(os.listdir(path)) > 0:
                print(f"Carpeta 'playlists' encontrada: {path}")
                return path
    return None

def get_launch_command():
    if os.path.exists("/usr/bin/retroarch"):
        return "retroarch"
    elif os.path.exists(os.path.expanduser("~/.var/app/org.libretro.RetroArch")):
        return "flatpak run org.libretro.RetroArch"
    elif os.path.exists(os.path.expanduser("~/snap/retroarch")):
        return "snap run retroarch"
    return "retroarch"

def process_thumbnails(thumbnails_path):
    home_path = os.path.expanduser("~/pegasus-frontend")  # Carpeta principal Pegasus
    os.makedirs(home_path, exist_ok=True)

    # Obtener todos los sistemas válidos primero
    valid_systems = []
    for system_folder in os.listdir(thumbnails_path):
        system_path = os.path.join(thumbnails_path, system_folder)
        if os.path.isdir(system_path):
            # Verificar si el sistema tiene un shortname definido
            shortname = SYSTEM_SHORTNAMES.get(system_folder)
            if not shortname:
                print(f"Sistema no reconocido: {system_folder}, saltando.")
                continue

            boxarts_path = os.path.join(system_path, "Named_Boxarts")
            snaps_path = os.path.join(system_path, "Named_Snaps")

            # Verificar que existan y tengan archivos .png
            if not (os.path.exists(boxarts_path) and os.listdir(boxarts_path)):
                continue
            if not (os.path.exists(snaps_path) and os.listdir(snaps_path)):
                continue

            valid_systems.append((system_folder, shortname, boxarts_path, snaps_path))

    # Usar tqdm para mostrar progreso general
    for system_folder, shortname, boxarts_path, snaps_path in tqdm(valid_systems, desc="Procesando sistemas", unit="sistema"):
        # Crear estructura en pegasus-frontend usando el shortname
        target_system_path = os.path.join(home_path, shortname, "media")
        os.makedirs(os.path.join(target_system_path, "boxFront"), exist_ok=True)
        os.makedirs(os.path.join(target_system_path, "screenshot"), exist_ok=True)
        os.makedirs(os.path.join(target_system_path, "videos"), exist_ok=True)
        os.makedirs(os.path.join(target_system_path, "wheel"), exist_ok=True)

        # Copiar imágenes de Boxarts
        copy_images(boxarts_path, os.path.join(target_system_path, "boxFront"))

        # Copiar imágenes de Snaps
        copy_images(snaps_path, os.path.join(target_system_path, "screenshot"))
    home_path = os.path.expanduser("~/pegasus-frontend")  # Carpeta principal Pegasus
    os.makedirs(home_path, exist_ok=True)

    valid_systems = []
    for system_folder in os.listdir(thumbnails_path):
        system_path = os.path.join(thumbnails_path, system_folder)
        if os.path.isdir(system_path):
            shortname = SYSTEM_SHORTNAMES.get(system_folder)
            if not shortname:
                print(f"Sistema no reconocido: {system_folder}, saltando.")
                continue

            boxarts_path = os.path.join(system_path, "Named_Boxarts")
            snaps_path = os.path.join(system_path, "Named_Snaps")

            if not (os.path.exists(boxarts_path) and os.listdir(boxarts_path)):
                continue
            if not (os.path.exists(snaps_path) and os.listdir(snaps_path)):
                continue

            valid_systems.append((system_folder, shortname, boxarts_path, snaps_path))

    for system_folder, shortname, boxarts_path, snaps_path in tqdm(valid_systems, desc="Procesando sistemas", unit="sistema"):
        target_system_path = os.path.join(home_path, shortname, "media")
        os.makedirs(os.path.join(target_system_path, "boxFront"), exist_ok=True)
        os.makedirs(os.path.join(target_system_path, "screenshot"), exist_ok=True)
        os.makedirs(os.path.join(target_system_path, "videos"), exist_ok=True)
        os.makedirs(os.path.join(target_system_path, "wheel"), exist_ok=True)

        copy_images(boxarts_path, os.path.join(target_system_path, "boxFront"))
        copy_images(snaps_path, os.path.join(target_system_path, "screenshot"))

def copy_images(src, dest):
    png_files = [f for f in os.listdir(src) if f.endswith(".png")]
    for file in tqdm(png_files, desc=f"Copiando imágenes en {os.path.basename(dest)}", unit="imagen", leave=False):
        shutil.copy2(os.path.join(src, file), dest)

def generate_metadata_files(playlists_path, pegasus_home):
    launch_cmd = get_launch_command()

    for playlist_file in tqdm(os.listdir(playlists_path), desc="Procesando playlists", unit="playlist"):
        if not playlist_file.endswith('.lpl'):
            continue

        system_name = playlist_file[:-4]
        shortname = SYSTEM_SHORTNAMES.get(system_name)

        if not shortname:
            print(f"Sistema no reconocido: {system_name}, saltando.")
            continue

        try:
            with open(os.path.join(playlists_path, playlist_file), 'r', encoding='utf-8') as f:
                playlist_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error leyendo playlist {playlist_file}: {e}")
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

            # Asegurarse de que la ruta comience con ./
            if rom_path.startswith('/'):
                rom_path = f".{rom_path}"  # Agregar punto al inicio si la ruta comienza con /
            elif not rom_path.startswith('./'):
                rom_path = f"./{rom_path}"  # Agregar ./ si la ruta no comienza con ninguno

            game_name = item.get('label', '')
            if not game_name or not rom_path:
                continue

            metadata_content.extend([
                f"game: {game_name}",
                f"file: {rom_path}",
                f"assets.boxFront: ./media/boxFront/{game_name}.png",
                f"assets.screenshot: ./media/screenshot/{game_name}.png",
                f"assets.videos: ./media/videos/{game_name}.mp4",
                f"assets.wheel: ./media/wheel/{game_name}.png\n"
            ])

        system_path = os.path.join(pegasus_home, shortname)
        os.makedirs(system_path, exist_ok=True)

        metadata_path = os.path.join(system_path, "metadata.txt")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata_content))

        print(f"Metadata generada para {system_name}")
    launch_cmd = get_launch_command()

    for playlist_file in tqdm(os.listdir(playlists_path), desc="Procesando playlists", unit="playlist"):
        if not playlist_file.endswith('.lpl'):
            continue

        system_name = playlist_file[:-4]  # Quitar extensión .lpl
        shortname = SYSTEM_SHORTNAMES.get(system_name)

        if not shortname:
            print(f"Sistema no reconocido: {system_name}, saltando.")
            continue

        try:
            with open(os.path.join(playlists_path, playlist_file), 'r', encoding='utf-8') as f:
                playlist_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error leyendo playlist {playlist_file}: {e}")
            continue

        if 'items' not in playlist_data:
            continue

        # Obtener core_path del primer elemento no DETECT
        core_path = "DETECT"
        for item in playlist_data['items']:
            if item.get('core_path') and item['core_path'] != "DETECT":
                core_path = item['core_path']
                break

        # Crear contenido del metadata.txt
        metadata_content = [
            f"collection: {system_name}",
            f"shortname: {shortname}",
            f"launch: {launch_cmd} -L {core_path} {{file.path}}\n"
        ]

        # Agregar entradas de juegos
        for item in playlist_data['items']:
            full_path = item.get('path', '')
            rom_path = full_path.split('#')[0] if '#' in full_path else full_path

            game_name = item.get('label', '')
            if not game_name or not rom_path:
                continue

            metadata_content.extend([
                f"game: {game_name}",
                f"file: .{rom_path}",  # Agregado el punto antes de la ruta
                f"assets.boxFront: ./media/boxFront/{game_name}.png",
                f"assets.screenshot: ./media/screenshot/{game_name}.png",
                f"assets.videos: ./media/videos/{game_name}.mp4",
                f"assets.wheel: ./media/wheel/{game_name}.png\n"
            ])

        # Escribir archivo metadata.txt
        system_path = os.path.join(pegasus_home, shortname)
        os.makedirs(system_path, exist_ok=True)

        metadata_path = os.path.join(system_path, "metadata.txt")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata_content))

        print(f"Metadata generada para {system_name}")
    launch_cmd = get_launch_command()

    for playlist_file in tqdm(os.listdir(playlists_path), desc="Procesando playlists", unit="playlist"):
        if not playlist_file.endswith('.lpl'):
            continue

        system_name = playlist_file[:-4]  # Quitar extensión .lpl
        shortname = SYSTEM_SHORTNAMES.get(system_name)

        if not shortname:
            print(f"Sistema no reconocido: {system_name}, saltando.")
            continue

        try:
            with open(os.path.join(playlists_path, playlist_file), 'r', encoding='utf-8') as f:
                playlist_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error leyendo playlist {playlist_file}: {e}")
            continue

        if 'items' not in playlist_data:
            continue

        # Obtener core_path del primer elemento no DETECT
        core_path = "DETECT"
        for item in playlist_data['items']:
            if item.get('core_path') and item['core_path'] != "DETECT":
                core_path = item['core_path']
                break

        # Crear contenido del metadata.txt
        metadata_content = [
            f"collection: {system_name}",
            f"shortname: {shortname}",
            f"launch: {launch_cmd} -L {core_path} {{file.path}}\n"
        ]

        # Agregar entradas de juegos
        for item in playlist_data['items']:
            full_path = item.get('path', '')
            rom_path = full_path.split('#')[0] if '#' in full_path else full_path

            game_name = item.get('label', '')
            if not game_name or not rom_path:
                continue

            metadata_content.extend([
                f"game: {game_name}",
                f"file: {rom_path}",
                f"assets.boxFront: ./media/boxFront/{game_name}.png",
                f"assets.screenshot: ./media/screenshot/{game_name}.png",
                f"assets.videos: ./media/videos/{game_name}.mp4",
                f"assets.wheel: ./media/wheel/{game_name}.png\n"
            ])

        # Escribir archivo metadata.txt
        system_path = os.path.join(pegasus_home, shortname)
        os.makedirs(system_path, exist_ok=True)

        metadata_path = os.path.join(system_path, "metadata.txt")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata_content))

        print(f"Metadata generada para {system_name}")

def main():
    # Paso 1: Encontrar RetroArch
    retroarch_base = find_retroarch()
    if not retroarch_base:
        print("RetroArch no encontrado. Terminando el script.")
        return

    # Paso 2: Encontrar la carpeta 'thumbnails'
    thumbnails_path = find_thumbnails_path(retroarch_base)
    if not thumbnails_path:
        print("Carpeta 'thumbnails' no encontrada. Terminando el script.")
        return

    # Paso 3: Encontrar la carpeta 'playlists'
    playlists_path = find_playlists_path()
    if not playlists_path:
        print("Carpeta 'playlists' no encontrada o vacía. Terminando el script.")
        return

    # Paso 4: Procesar carpetas de sistemas y thumbnails
    home_path = os.path.expanduser("~/pegasus-frontend")
    process_thumbnails(thumbnails_path)

    # Paso 5: Generar archivos metadata.txt
    generate_metadata_files(playlists_path, home_path)

    print("Script completado exitosamente.")

if __name__ == "__main__":
    main()
