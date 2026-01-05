import os
import sys
import subprocess
import time
import shutil
import json
from pathlib import Path

# Coba import colorama, jika belum ada, pakai fallback
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore: 
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
        LIGHTBLACK_EX = "" 
    class Style: 
        BRIGHT = DIM = RESET_ALL = ""

TOOLS = {
    "1": ("Spotify Student Verification", "spotify-verify-tool"),
    "2": ("Veterans / Military Verification", "veterans-verify-tool"),
    "3": ("YouTube Student Verification", "youtube-verify-tool"),
    "4": ("Perplexity Verification", "perplexity-verify-tool"),
    "5": ("K12 Student/Teacher Verification", "k12-verify-tool"),
    "6": ("One Verify Tool", "one-verify-tool"),
    "7": ("Bolt.new Verification", "boltnew-verify-tool"),
}

def get_terminal_width():
    return shutil.get_terminal_size().columns

def center_text(text):
    width = get_terminal_width()
    try:
        clean_text = text.replace(Fore.RED, "").replace(Fore.YELLOW, "").replace(Fore.GREEN, "").replace(Fore.CYAN, "").replace(Fore.BLUE, "").replace(Fore.MAGENTA, "").replace(Fore.WHITE, "").replace(Fore.LIGHTBLACK_EX, "").replace(Style.BRIGHT, "").replace(Style.RESET_ALL, "")
        padding = max(0, (width - len(clean_text)) // 2)
        return " " * padding + text
    except:
        return text.center(width)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_rainbow_banner():
    banner_art = [
        r"██████╗  ██████╗  ██████╗ ████████╗███████╗███████╗ ██████╗ ",
        r"██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔════╝██╔════╝ ",
        r"██████╔╝██║   ██║██║   ██║   ██║   ███████╗█████╗  ██║      ",
        r"██╔══██╗██║   ██║██║   ██║   ██║   ╚════██║██╔══╝  ██║      ",
        r"██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████║███████╗╚██████╗ ",
        r"╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚══════╝ ╚═════╝ ",
        r"                  VERIFICATION  BOT                         "
    ]
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    
    print("\n")
    for i, line in enumerate(banner_art):
        color = colors[i % len(colors)]
        print(center_text(f"{Style.BRIGHT}{color}{line}"))
    print(center_text(f"{Fore.WHITE}Created by Toko RootSec Bot"))
    print("\n" + center_text(f"{Fore.LIGHTBLACK_EX}{'='*60}"))
    print("")

def setup_telegram():
    """Setup Konfigurasi Telegram"""
    clear_screen()
    print(f"\n{center_text(Fore.YELLOW + '╔════════════════════════════════════════╗')}")
    print(f"{center_text(Fore.YELLOW + '║     SETUP NOTIFIKASI TELEGRAM BOT      ║')}")
    print(f"{center_text(Fore.YELLOW + '╚════════════════════════════════════════╝')}\n")
    
    print(f"{Fore.CYAN}Panduan Singkat:{Style.RESET_ALL}")
    print(f"1. Chat {Fore.GREEN}@BotFather{Style.RESET_ALL} di Telegram, buat bot baru, salin {Fore.YELLOW}TOKEN{Style.RESET_ALL}.")
    print(f"2. Chat {Fore.GREEN}@userinfobot{Style.RESET_ALL} untuk mendapatkan {Fore.YELLOW}ID{Style.RESET_ALL} (User ID) Anda.\n")
    
    print(f"{Fore.LIGHTBLACK_EX}{'-'*60}{Style.RESET_ALL}")
    token = input(f"{Fore.GREEN}[?] Masukkan Bot Token : {Style.RESET_ALL}").strip()
    chat_id = input(f"{Fore.GREEN}[?] Masukkan Chat ID   : {Style.RESET_ALL}").strip()
    
    if not token or not chat_id:
        print(f"\n{Fore.RED}[ERROR] Token dan Chat ID tidak boleh kosong!{Style.RESET_ALL}")
        time.sleep(2)
        return

    config_data = {"token": token, "chat_id": chat_id}
    
    try:
        with open("telegram.json", "w") as f:
            json.dump(config_data, f, indent=4)
        print(f"\n{Fore.GREEN}[SUCCESS] Konfigurasi tersimpan di 'telegram.json'!{Style.RESET_ALL}")
        print(f"Notifikasi akan dikirim otomatis jika verifikasi berhasil.")
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] Gagal menyimpan file: {e}{Style.RESET_ALL}")
    
    time.sleep(3)

def show_tutorial():
    clear_screen()
    print(f"\n{center_text(Fore.YELLOW + '╔════════════════════════════════════════╗')}")
    print(f"{center_text(Fore.YELLOW + '║      PANDUAN PENGGUNAAN SCRIPT         ║')}")
    print(f"{center_text(Fore.YELLOW + '╚════════════════════════════════════════╝')}\n")
    print(f"{Fore.CYAN}1. INSTALASI LIBRARY{Style.RESET_ALL}")
    print(f"   Ketik: {Fore.GREEN}pip install -r requirements.txt{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}2. SETUP NOTIFIKASI (BARU){Style.RESET_ALL}")
    print(f"   Pilih menu {Fore.MAGENTA}[9]{Style.RESET_ALL} untuk mengatur Bot Telegram.")
    print(f"   Script akan otomatis mengirim pesan jika verifikasi Sukses.\n")
    print(f"{Fore.LIGHTBLACK_EX}{'-'*60}{Style.RESET_ALL}")
    input(center_text(f"Tekan {Fore.GREEN}[ENTER]{Style.RESET_ALL} untuk kembali..."))

def run_script(folder_name):
    target_folder = Path.cwd() / folder_name
    target_script = target_folder / "main.py"
    if not target_folder.exists():
        print(center_text(f"{Fore.RED}[ERROR] Folder '{folder_name}' tidak ditemukan!"))
        time.sleep(2); return
    if not target_script.exists():
        print(center_text(f"{Fore.RED}[ERROR] File 'main.py' tidak ditemukan di '{folder_name}'!"))
        time.sleep(2); return

    original_cwd = os.getcwd()
    try:
        os.chdir(target_folder)
        clear_screen()
        print(f"{Fore.CYAN}[*] RootSec Launcher >> {folder_name} ...{Style.RESET_ALL}\n")
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Dihentikan oleh user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")
    finally:
        os.chdir(original_cwd)
        print(f"\n{Fore.LIGHTBLACK_EX}{'-'*50}{Style.RESET_ALL}")
        input(center_text("Tekan [ENTER] untuk kembali ke Menu Utama..."))

def main():
    while True:
        clear_screen()
        print_rainbow_banner()
        print(center_text(f"{Fore.YELLOW}PILIH TOOLS VERIFIKASI:{Style.RESET_ALL}"))
        print("")
        for key, (name, _) in TOOLS.items():
            print(center_text(f"{Fore.CYAN}{key.center(3)} {Fore.WHITE}- {name}"))
        print("")
        print(center_text(f"{Fore.GREEN}[8]   PANDUAN / TUTORIAL{Style.RESET_ALL}"))
        print(center_text(f"{Fore.MAGENTA}[9]   SETTING TELEGRAM NOTIF{Style.RESET_ALL}"))
        print(center_text(f"{Fore.RED}[0]   KELUAR / EXIT     {Style.RESET_ALL}"))
        print("")
        print(center_text(f"{Fore.LIGHTBLACK_EX}{'='*60}"))
        
        sys.stdout.write(f"\n{Fore.GREEN}RootSec@Bot ~# {Style.RESET_ALL}")
        choice = input().strip()

        if choice == '0':
            print(f"\n{Fore.MAGENTA}Bye!{Style.RESET_ALL}"); sys.exit()
        elif choice == '8':
            show_tutorial()
        elif choice == '9':
            setup_telegram()
        elif choice in TOOLS:
            _, folder = TOOLS[choice]
            run_script(folder)
        else:
            print(f"\n{Fore.RED} [!] Pilihan salah.{Style.RESET_ALL}"); time.sleep(1)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit()
