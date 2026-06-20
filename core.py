import os
import platform
import json
import re
import shutil
import logging


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


def _noop(_msg):
    pass


def setup_logging(output_path):
    log_file = os.path.join(output_path, "retropegasus.log")
    logger = logging.getLogger("retropegasus")
    logger.handlers.clear()
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def get_system_paths():
    system = platform.system()
    home   = os.path.expanduser("~")

    if system == "Linux":
        return [
            os.path.join(home, ".var", "app", "org.libretro.RetroArch",
                         "config", "retroarch"),
            os.path.join(home, "snap", "retroarch", "current", ".config",
                         "retroarch"),
            os.path.join(home, ".config", "retroarch"),
            "/etc/retroarch",
        ]

    if system == "Windows":
        appdata = os.getenv("APPDATA", "")
        localappdata = os.getenv("LOCALAPPDATA", "")
        return [
            os.path.join(appdata, "RetroArch"),
            os.path.join(localappdata, "RetroArch"),
            r"C:\RetroArch-Win64",
            r"C:\RetroArch-Win32",
            r"C:\RetroArch",
            os.path.join(os.getenv("ProgramFiles", r"C:\Program Files"), "RetroArch"),
            os.path.join(os.getenv("ProgramFiles(x86)", r"C:\Program Files (x86)"), "RetroArch"),
        ]

    if system == "Darwin":
        return [
            os.path.join(home, "Library", "Application Support", "RetroArch"),
            os.path.join(home, "Applications", "RetroArch.app",
                         "Contents", "Resources", "RetroArch"),
            "/Applications/RetroArch.app/Contents/Resources/RetroArch",
        ]

    return []


def find_retroarch_candidates(on_progress=_noop):
    candidates = []
    for path in get_system_paths():
        on_progress(f"Checking: {path}")
        if os.path.isdir(path):
            is_valid, _ = verify_retroarch_folders(path)
            if is_valid:
                candidates.append(path)
    return candidates


def verify_retroarch_folders(path):
    required = {"thumbnails": False, "playlists": False}
    errors   = []
    for folder in required:
        fp = os.path.join(path, folder)
        if os.path.isdir(fp):
            if os.listdir(fp):
                required[folder] = True
            else:
                errors.append(f"The '{folder}' folder is empty")
        else:
            errors.append(f"The '{folder}' folder was not found")
    return all(required.values()), errors


def find_thumbnails_path(retroarch_path):
    p = os.path.join(retroarch_path, "thumbnails")
    return p if os.path.isdir(p) else None


def find_playlists_path(retroarch_path):
    p = os.path.join(retroarch_path, "playlists")
    return p if os.path.isdir(p) else None


def list_playlists(playlists_path):
    if not playlists_path or not os.path.isdir(playlists_path):
        return []
    return sorted(
        f[:-4] for f in os.listdir(playlists_path) if f.endswith(".lpl")
    )


def get_launch_command(retroarch_path=""):
    system = platform.system()
    home   = os.path.expanduser("~")

    if system == "Linux":
        flatpak_config = os.path.join(
            home, ".var", "app", "org.libretro.RetroArch", "config", "retroarch")
        snap_config = os.path.join(
            home, "snap", "retroarch", "current", ".config", "retroarch")

        norm = os.path.normpath(retroarch_path)

        if norm == os.path.normpath(flatpak_config):
            return "flatpak run org.libretro.RetroArch"
        if norm == os.path.normpath(snap_config):
            return "snap run retroarch"
        return "retroarch"

    if system == "Windows":
        if retroarch_path:
            exe = os.path.join(retroarch_path, "retroarch.exe")
            if os.path.isfile(exe):
                return f'"{exe}"'
        return "retroarch.exe"

    if system == "Darwin":
        candidates = [
            "/Applications/RetroArch.app/Contents/MacOS/retroarch",
            os.path.join(home, "Applications",
                         "RetroArch.app", "Contents", "MacOS", "retroarch"),
        ]
        for c in candidates:
            if os.path.isfile(c):
                return c
        return "retroarch"

    return "retroarch"


def sanitize_filename(name):
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    name = name.strip(". ")
    return name or "_"


def detect_core_mode(playlist_data, system_name, logger=None):
    cores = set()
    for item in playlist_data.get("items", []):
        cp = item.get("core_path", "").strip()
        if cp and cp != "DETECT":
            cores.add(cp)

    default_core = playlist_data.get("default_core_path", "").strip()
    if default_core and default_core != "DETECT":
        cores.add(default_core)

    if not cores:
        msg = f"{system_name}: No cores found. Using global DETECT."
        if logger: logger.info(msg)
        return "DETECT", False
    if len(cores) == 1:
        global_core = cores.pop()
        msg = f"{system_name}: All games share the same core: {global_core}"
        if logger: logger.info(msg)
        return global_core, False
    else:
        msg = f"{system_name}: Multiple cores detected ({', '.join(cores)}). Using per-game launch."
        if logger: logger.info(msg)
        return None, True


def _normalize_rom_path(full_path, system_type):
    rom_path = full_path.split("#")[0] if "#" in full_path else full_path

    if system_type == "Windows":
        if rom_path.startswith("./"):
            rom_path = rom_path[2:]
        if rom_path.startswith("/"):
            rom_path = rom_path[1:]
        rom_path = rom_path.replace("/", "\\")
        if not re.match(r"^[A-Za-z]:\\", rom_path):
            rom_path = "C:\\" + rom_path
    else:
        if rom_path.startswith("./"):
            rom_path = rom_path[2:]
        if not rom_path.startswith("/"):
            rom_path = "/" + rom_path
        rom_path = rom_path.replace("\\", "/")

    return rom_path


def generate_metadata(playlists_path, pegasus_home, logger,
                       retroarch_path="",
                       selected_systems=None,
                       thumbnails_base_path=None, copy_media=False,
                       on_progress=_noop, should_cancel=None):
    include_media = thumbnails_base_path is not None
    media_desc = "no media"
    if include_media:
        media_desc = "copying media" if copy_media else "absolute media paths"
    logger.info(f"=== Generating metadata.txt files ({media_desc}) ===")

    launch_cmd_base = get_launch_command(retroarch_path)
    logger.info(f"Launch command detected: {launch_cmd_base}")
    system_type     = platform.system()

    all_playlist_files = [
        f for f in os.listdir(playlists_path) if f.endswith(".lpl")
    ]
    if selected_systems is not None:
        playlist_files = [f for f in all_playlist_files if f[:-4] in selected_systems]
    else:
        playlist_files = all_playlist_files

    total_playlists = len(playlist_files)
    logger.info(
        f"Found {total_playlists} playlist files to process "
        f"(out of {len(all_playlist_files)} total)"
    )
    on_progress(f"Processing {total_playlists} playlist files")

    processed    = 0
    total_games  = 0
    skipped      = []
    per_system   = []
    media_copied = 0
    media_errors = 0

    for idx, playlist_file in enumerate(playlist_files, 1):
        if should_cancel and should_cancel():
            on_progress("Cancelled by user.")
            logger.warning("Process cancelled by user.")
            break

        system_name = playlist_file[:-4]
        on_progress(f"[{idx}/{total_playlists}] Processing: {system_name}")
        logger.info(f"--- Processing playlist: {system_name} ---")

        shortname = SYSTEM_SHORTNAMES.get(system_name)
        if not shortname:
            msg = f"System not recognized: {system_name}, skipping."
            logger.warning(msg)
            on_progress(f"  {msg}")
            skipped.append(system_name)
            continue

        try:
            with open(
                os.path.join(playlists_path, playlist_file), "r", encoding="utf-8"
            ) as f:
                playlist_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error reading playlist {playlist_file}: {e}")
            on_progress(f"  Error reading playlist: {e}")
            continue

        if not playlist_data.get("items"):
            logger.warning(f"No items in {playlist_file}")
            on_progress("  No games found in this playlist, skipping.")
            continue

        global_core, use_individual = detect_core_mode(
            playlist_data, system_name, logger=logger
        )

        metadata_content = [
            f"collection: {system_name}",
            f"shortname: {shortname}",
        ]
        if not use_individual:
            metadata_content.append(
                f"launch: {launch_cmd_base} -L {global_core} {{file.path}}"
            )
        metadata_content.append("")

        system_path = os.path.join(pegasus_home, shortname)
        os.makedirs(system_path, exist_ok=True)

        games_count = 0
        for item in playlist_data["items"]:
            if should_cancel and should_cancel():
                break

            full_path = item.get("path", "")
            rom_path  = _normalize_rom_path(full_path, system_type)
            game_name = item.get("label", "")
            if not game_name or not rom_path:
                continue

            games_count += 1
            total_games += 1

            game_metadata = [f"game: {game_name}", f"file: {rom_path}"]

            if use_individual:
                core_for_game = item.get("core_path", "").strip()
                if not core_for_game or core_for_game == "DETECT":
                    default_core = playlist_data.get("default_core_path", "").strip()
                    if default_core and default_core != "DETECT":
                        core_for_game = default_core
                        logger.info(
                            f"Game '{game_name}' has no core, "
                            f"using default_core_path: {default_core}"
                        )
                    else:
                        core_for_game = "DETECT"
                        logger.warning(
                            f"Game '{game_name}' has no core defined, using DETECT"
                        )
                game_metadata.append(
                    f"launch: {launch_cmd_base} -L {core_for_game} {{file.path}}"
                )

            if include_media:
                for retroarch_media, pegasus_media in MEDIA_MAPPING.items():
                    source_path = os.path.join(
                        thumbnails_base_path, system_name,
                        retroarch_media, f"{game_name}.png"
                    )
                    if not os.path.exists(source_path):
                        continue

                    if copy_media:
                        safe_name = sanitize_filename(game_name)
                        dest_dir  = os.path.join(system_path, "media", pegasus_media)
                        dest_path = os.path.join(dest_dir, f"{safe_name}.png")
                        try:
                            os.makedirs(dest_dir, exist_ok=True)
                            shutil.copy2(source_path, dest_path)
                            media_copied += 1
                            relative_path = f"media/{pegasus_media}/{safe_name}.png"
                            game_metadata.append(
                                f"assets.{pegasus_media}: {relative_path}"
                            )
                        except OSError as e:
                            media_errors += 1
                            logger.warning(
                                f"Could not copy media for '{game_name}' "
                                f"({pegasus_media}): {e}"
                            )
                    else:
                        game_metadata.append(
                            f"assets.{pegasus_media}: {source_path}"
                        )

            game_metadata.append("")
            metadata_content.extend(game_metadata)

        metadata_path = os.path.join(system_path, "metadata.txt")
        with open(metadata_path, "w", encoding="utf-8") as f:
            f.write("\n".join(metadata_content))

        processed += 1
        mode_desc = (
            "per-game cores" if use_individual else f"global core: {global_core}"
        )
        logger.info(
            f"Generated {system_name} with {games_count} games ({mode_desc})"
        )
        on_progress(
            f"  Generated {system_name} with {games_count} games ({mode_desc})"
        )

        per_system.append({
            "system":           system_name,
            "shortname":        shortname,
            "games":            games_count,
            "individual_cores": use_individual,
            "global_core":      global_core,
        })

    logger.info(
        f"=== Finished processing {processed} playlists, "
        f"total games: {total_games} ==="
    )
    if copy_media:
        logger.info(
            f"Media files copied: {media_copied}, errors: {media_errors}"
        )
        on_progress(
            f"Media files copied: {media_copied} (errors: {media_errors})"
        )

    return {
        "processed":    processed,
        "total_games":  total_games,
        "skipped":      skipped,
        "media_copied": media_copied,
        "media_errors": media_errors,
        "per_system":   per_system,
    }
