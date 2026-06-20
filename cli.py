import os
import sys
import core

def _ansi_supported():
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                if kernel32.SetConsoleMode(handle, mode.value | 0x0004):
                    return True
        except Exception:
            pass
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


if _ansi_supported():
    class Colors:
        CYAN = '\033[96m'
        YELLOW = '\033[93m'
        GREEN = '\033[92m'
        RED = '\033[91m'
        RESET = '\033[0m'
else:
    class Colors:
        CYAN = ''
        YELLOW = ''
        GREEN = ''
        RED = ''
        RESET = ''


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


def cli_progress(message):
    print(f"{Colors.CYAN}{message}{Colors.RESET}")


def get_output_path():
    while True:
        os_label = "Windows" if sys.platform == "win32" else "Linux/macOS"
        default_path = os.path.join(os.path.expanduser("~"), "pegasus-frontend")
        print(f"\n{Colors.YELLOW}Select the location to save Pegasus Frontend data:{Colors.RESET}")
        print(f"{Colors.YELLOW}[1]{Colors.RESET} Use default location on {os_label} ({default_path})")
        print(f"{Colors.YELLOW}[2]{Colors.RESET} Specify custom path")

        choice = input(f"\n{Colors.YELLOW}Select an option (1-2): {Colors.RESET}")

        if choice == "1":
            output_path = os.path.join(os.path.expanduser("~"), "pegasus-frontend")
        elif choice == "2":
            base_path = input(f"\n{Colors.YELLOW}Enter the output path (this folder will be used as-is): {Colors.RESET}")
            base_path = os.path.normpath(os.path.expanduser(base_path))

            if not os.path.exists(base_path):
                print(f"{Colors.RED}The path {base_path} does not exist.{Colors.RESET}")
                continue

            output_path = base_path
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


def find_retroarch_auto():
    found_paths = core.find_retroarch_candidates(on_progress=cli_progress)

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

        is_valid, errors = core.verify_retroarch_folders(path)

        if not is_valid:
            print(f"\n{Colors.RED}The path does not contain a valid RetroArch installation:{Colors.RESET}")
            for error in errors:
                print(f"{Colors.RED}• {error}{Colors.RESET}")

            retry = input(f"\n{Colors.YELLOW}Would you like to try another path? (y/n): {Colors.RESET}").lower()
            if retry != 'y':
                return None
            continue

        return path


def get_media_handling_mode():
    while True:
        print(f"\n{Colors.YELLOW}How do you want to handle media files (images)?{Colors.RESET}")
        print(f"{Colors.YELLOW}[1]{Colors.RESET} Use absolute paths (recommended) - No files copied, uses RetroArch thumbnails directly")
        print(f"{Colors.YELLOW}[2]{Colors.RESET} Copy media files into the Pegasus collection folder (portable, takes longer)")
        print(f"{Colors.YELLOW}[3]{Colors.RESET} Skip media files")

        choice = input(f"\n{Colors.YELLOW}Select an option (1-3): {Colors.RESET}")
        if choice in ('1', '2', '3'):
            return choice
        print(f"{Colors.RED}Invalid option. Please select 1, 2 or 3.{Colors.RESET}")


def select_playlists(playlists_path):
    playlist_systems = core.list_playlists(playlists_path)

    print(f"\n{Colors.CYAN}Available collections:{Colors.RESET}")
    for i, system_name in enumerate(playlist_systems, 1):
        print(f"{Colors.YELLOW}[{i}]{Colors.RESET} {system_name}")

    print(f"\n{Colors.CYAN}Selection format:{Colors.RESET}")
    print("    • 'a' or '0'  → process all")
    print("    • '1,3,5'     → process collections 1, 3, and 5")
    print("    • '2-4'       → process collections 2, 3, and 4")
    print("    • '1,3-5,7'   → process 1, 3, 4, 5, and 7")

    while True:
        choice = input(f"\n{Colors.YELLOW}Your selection: {Colors.RESET}").strip()

        if choice.lower() in ('a', '0'):
            return playlist_systems

        selected_indices = set()
        parts = choice.split(',')
        valid = True
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = part.split('-')
                    start, end = int(start.strip()), int(end.strip())
                    if start < 1 or end > len(playlist_systems) or start > end:
                        print(f"{Colors.RED}Invalid range: {part}. Please try again.{Colors.RESET}")
                        valid = False
                        break
                    selected_indices.update(range(start, end + 1))
                except ValueError:
                    print(f"{Colors.RED}Invalid range: {part}. Please try again.{Colors.RESET}")
                    valid = False
                    break
            else:
                try:
                    num = int(part)
                    if num < 1 or num > len(playlist_systems):
                        print(f"{Colors.RED}Number {num} is out of range (1-{len(playlist_systems)}). Please try again.{Colors.RESET}")
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

        return [playlist_systems[idx - 1] for idx in sorted(selected_indices)]


def run():
    total_playlists = 0
    total_games = 0
    logger = None

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

            thumbnails_path = core.find_thumbnails_path(retroarch_path)
            if not thumbnails_path:
                print(f"{Colors.RED}The 'thumbnails' folder was not found at the specified path.{Colors.RESET}")
                input("\nPress Enter to continue...")
                continue

            playlists_path = core.find_playlists_path(retroarch_path)
            if not playlists_path:
                print(f"{Colors.RED}The 'playlists' folder was not found at the specified path.{Colors.RESET}")
                input("\nPress Enter to continue...")
                continue

            output_path = get_output_path()

            logger = core.setup_logging(output_path)
            logger.info("=== RetroPegasus Converter Tool Started (CLI) ===")
            logger.info(f"Output path: {output_path}")
            logger.info(f"RetroArch path: {retroarch_path}")

            selected_systems = select_playlists(playlists_path)
            if not selected_systems:
                print(f"{Colors.RED}No collections selected. Aborting.{Colors.RESET}")
                input("\nPress Enter to continue...")
                continue

            logger.info(f"Selected collections: {', '.join(selected_systems)}")

            media_mode = get_media_handling_mode()
            logger.info(f"Media handling mode: {media_mode}")

            thumbnails_base = None
            copy_media = False
            if media_mode == '1':
                thumbnails_base = thumbnails_path
                print(f"\n{Colors.CYAN}Using absolute paths for media (recommended){Colors.RESET}")
            elif media_mode == '2':
                thumbnails_base = thumbnails_path
                copy_media = True
                print(f"\n{Colors.CYAN}Copying media files into the Pegasus collection folder...{Colors.RESET}")
            else:
                print(f"\n{Colors.CYAN}Skipping media files...{Colors.RESET}")

            result = core.generate_metadata(
                playlists_path, output_path, logger,
                retroarch_path=retroarch_path,
                selected_systems=selected_systems,
                thumbnails_base_path=thumbnails_base,
                copy_media=copy_media,
                on_progress=cli_progress,
            )

            total_playlists += result["processed"]
            total_games += result["total_games"]

            print(f"\n{Colors.GREEN}✓ Conversion completed successfully!{Colors.RESET}")
            print(f"{Colors.CYAN}Total playlists processed: {total_playlists}{Colors.RESET}")
            print(f"{Colors.CYAN}Total games: {total_games}{Colors.RESET}")
            if copy_media:
                print(f"{Colors.CYAN}Media files copied: {result['media_copied']} (errors: {result['media_errors']}){Colors.RESET}")
            input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}See you later!{Colors.RESET}")
            if logger:
                logger.info("Process interrupted by user.")
            sys.exit(0)


if __name__ == "__main__":
    run()
