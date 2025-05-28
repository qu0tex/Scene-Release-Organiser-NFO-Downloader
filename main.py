import os
import sys
import argparse
import subprocess
import shutil
from multiprocessing import Pool, cpu_count
from functools import partial
from colorama import init, Fore, Style

init(autoreset=True)

SEVENZIP = r"C:\Program Files\7-Zip\7z.exe"
WINRAR = r"C:\Program Files\WinRAR\rar.exe"
PYTHON = r"C:\Python313\python.exe"

def validate_path(path):
    if not os.path.isdir(path):
        print(Fore.RED + f"[ERROR] Path does not exist: {path}")
        sys.exit(1)

def extract_diz_for_folder(folder, target_path):
    full_path = os.path.join(target_path, folder)
    if not os.path.isdir(full_path):
        return

    print(Fore.CYAN + f"[INFO] Processing: {folder}")
    diz_path = os.path.join(full_path, "file_id.diz")
    if os.path.exists(diz_path):
        print(Fore.GREEN + f"[OK] file_id.diz already exists in {folder}")
        return

    for ext in ('.zip', '.rar'):
        for file in os.listdir(full_path):
            if file.lower().endswith(ext):
                archive_path = os.path.join(full_path, file)
                print(Fore.YELLOW + f"[INFO] Found archive: {archive_path}")
                result = subprocess.run([
                    SEVENZIP, "e", archive_path,
                    f"-o{full_path}", "file_id.diz", "-aos"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(diz_path):
                    print(Fore.GREEN + f"[OK] Extracted file_id.diz in {folder}")
                    return
    print(Fore.RED + f"[ERROR] No file_id.diz found in {folder}")

def extract_file_id_diz(target_path):
    print(Fore.MAGENTA + "\n[INFO] Extracting file_id.diz files...")
    folders = os.listdir(target_path)
    with Pool(min(8, cpu_count())) as pool:
        pool.map(partial(extract_diz_for_folder, target_path=target_path), folders)

def move_foreign_for_folder(folder, target_path):
    full_path = os.path.join(target_path, folder)
    if not os.path.isdir(full_path) or folder == "_foreign":
        return

    foreign_langs = [
        "GERMAN", "FRENCH", "SPANISH", "DUTCH", "ITALIAN", "PORTUGUESE", "BULGARIAN", "SWEDISH",
        "DANISH", "NORWEGIAN", "FINNISH", "GREEK", "CZECH", "POLISH", "RUSSIAN", "TURKISH",
        "HUNGARIAN", "LITHUANIAN", "ROMANIAN", "LATVIAN", "SLOVAK", "ESTONIAN", "CHINESE",
        "JAPANESE", "KOREAN", "THAI", "INDONESIAN", "ARABIC", "HINDI", "BASQUE", "CATALAN",
        "SERBIAN", "CROATIAN", "SLOVENIAN", "UKRAINIAN", "HEBREW", "MALAY", "VIETNAMESE",
        "PERSIAN", "BENGALI", "JAP"
    ]

    is_foreign = False
    diz_path = os.path.join(full_path, "file_id.diz")
    if os.path.exists(diz_path):
        with open(diz_path, errors='ignore') as f:
            content = f.read().upper()
            if any(lang in content for lang in foreign_langs):
                is_foreign = True
    elif any(lang in folder.upper() for lang in foreign_langs):
        is_foreign = True

    if is_foreign:
        foreign_dir = os.path.join(target_path, "_foreign")
        os.makedirs(foreign_dir, exist_ok=True)
        shutil.move(full_path, os.path.join(foreign_dir, folder))
        print(Fore.YELLOW + f"[MOVED] Foreign release: {folder}")

def move_foreign_releases(target_path):
    print(Fore.MAGENTA + "\n[INFO] Moving foreign releases to _foreign...")
    folders = os.listdir(target_path)
    with Pool(min(8, cpu_count())) as pool:
        pool.map(partial(move_foreign_for_folder, target_path=target_path), folders)

def move_gamerip_for_folder(folder, target_path):
    full_path = os.path.join(target_path, folder)
    if not os.path.isdir(full_path) or folder == "_gamerips":
        return

    groups = ["-RAZOR", "-VACE", "-Unleashed", "-rG", "-bADkARMA", "-DELiGHT", "-OUTLAWS", "-RAiN"]
    if any(folder.endswith(group) for group in groups):
        gamerip_dir = os.path.join(target_path, "_gamerips")
        os.makedirs(gamerip_dir, exist_ok=True)
        shutil.move(full_path, os.path.join(gamerip_dir, folder))
        print(Fore.YELLOW + f"[MOVED] Gamerip: {folder}")

def move_gamerips(target_path):
    print(Fore.MAGENTA + "\n[INFO] Moving gamerip releases to _gamerips...")
    folders = os.listdir(target_path)
    with Pool(min(8, cpu_count())) as pool:
        pool.map(partial(move_gamerip_for_folder, target_path=target_path), folders)

def download_unleashed_nfos(target_path):
    print(Fore.MAGENTA + "\n[*] Downloading Unleashed NFOs...")
    subprocess.run([
        PYTHON,
        os.path.join(os.path.dirname(__file__), "download_unleashed_nfo.py"),
        target_path
    ])

def main():
    parser = argparse.ArgumentParser(description="0day/eBook Processing Tool v0.2 by Quotex")
    parser.add_argument('--path', required=True, help="Path to the folder to process")
    parser.add_argument('--extract', action='store_true', help="Extract file_id.diz")
    parser.add_argument('--moveforeign', action='store_true', help="Move foreign releases to _foreign")
    parser.add_argument('--unleashed', action='store_true', help="Download Unleashed NFOs")
    parser.add_argument('--gamerips', action='store_true', help="Move 0day gamerips to _gamerips")

    args = parser.parse_args()
    target_path = os.path.abspath(args.path)
    validate_path(target_path)

    if args.extract:
        extract_file_id_diz(target_path)
    if args.moveforeign:
        move_foreign_releases(target_path)
    if args.unleashed:
        download_unleashed_nfos(target_path)
    if args.gamerips:
        move_gamerips(target_path)

    print(Fore.GREEN + "\n[DONE] Processing complete.")

if __name__ == '__main__':
    main()
