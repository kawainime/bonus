import os
import sys
import subprocess
import time
import shutil
from pathlib import Path

# Coba import colorama, jika belum ada, pakai fallback
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Definisi class dummy jika colorama tidak terinstall
    class Fore: 
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
        LIGHTBLACK_EX = "" # Fallback untuk warna abu-abu
    class Style: 
        BRIGHT = DIM = RESET_ALL = ""

# Konfigurasi Tool dan Folder
# Format: "Nama Tampilan": "Nama Folder"
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
    return text.center(width)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_rainbow_banner():
    """Menampilkan Banner RootSec Bot berwarna-warni"""
    
    # ASCII Art untuk "RootSec Bot"
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
        # Rotasi warna untuk setiap baris
        color = colors[i % len(colors)]
        print(center_text(f"{Style.BRIGHT}{color}{line}"))
    print(center_text(f"{Fore.WHITE}Developer By Toko RootSec Bot"))
    # PERBAIKAN DI SINI: Menggunakan LIGHTBLACK_EX
    print("\n" + center_text(f"{Fore.LIGHTBLACK_EX}{'='*60}"))
    print("")

def run_script(folder_name):
    target_folder = Path.cwd() / folder_name
    target_script = target_folder / "main.py"

    if not target_folder.exists():
        print(center_text(f"{Fore.RED}[ERROR] Folder '{folder_name}' tidak ditemukan!"))
        time.sleep(2)
        return

    if not target_script.exists():
        print(center_text(f"{Fore.RED}[ERROR] File 'main.py' tidak ditemukan di '{folder_name}'!"))
        time.sleep(2)
        return

    original_cwd = os.getcwd()

    try:
        os.chdir(target_folder)
        clear_screen()
        # Banner kecil saat tool berjalan
        print(f"{Fore.CYAN}[*] RootSec Launcher >> {folder_name} ...{Style.RESET_ALL}\n")
        
        subprocess.run([sys.executable, "main.py"])
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Dihentikan oleh user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")
    finally:
        os.chdir(original_cwd)
        # PERBAIKAN DI SINI: Menggunakan LIGHTBLACK_EX
        print(f"\n{Fore.LIGHTBLACK_EX}{'-'*50}{Style.RESET_ALL}")
        input(center_text("Tekan [ENTER] untuk kembali ke Menu Utama..."))

def main():
    while True:
        clear_screen()
        print_rainbow_banner()
        
        print(center_text(f"{Fore.YELLOW}PILIH TOOLS VERIFIKASI:{Style.RESET_ALL}"))
        print("")

        # Menampilkan menu dengan rapi di tengah
        for key, (name, _) in TOOLS.items():
            # Kita buat sedikit padding manual agar terlihat seperti list tapi tetap di tengah
            print(center_text(f"{Fore.CYAN}{key.center(3)} {Fore.WHITE}- {name}"))
        
        print("")
        print(center_text(f"{Fore.RED}[0]  KELUAR / EXIT"))
        print("")
        # PERBAIKAN DI SINI: Menggunakan LIGHTBLACK_EX
        print(center_text(f"{Fore.LIGHTBLACK_EX}{'='*60}"))
        
        # Input prompt
        sys.stdout.write(f"\n{Fore.GREEN}RootSec@Bot ~# {Style.RESET_ALL}")
        choice = input().strip()

        if choice == '0':
            print(f"\n{Fore.MAGENTA}Terima kasih telah menggunakan RootSec Bot. Bye!{Style.RESET_ALL}")
            sys.exit()
        
        if choice in TOOLS:
            _, folder = TOOLS[choice]
            run_script(folder)
        else:
            print(f"\n{Fore.RED} [!] Pilihan salah. Masukkan angka 0-7.{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Force Close.{Style.RESET_ALL}")
        sys.exit()
