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
        LIGHTBLACK_EX = "" 
    class Style: 
        BRIGHT = DIM = RESET_ALL = ""

# Konfigurasi Tool dan Folder
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
        # Menghapus kode warna ANSI untuk perhitungan panjang string yang akurat
        clean_text = text.replace(Fore.RED, "").replace(Fore.YELLOW, "").replace(Fore.GREEN, "").replace(Fore.CYAN, "").replace(Fore.BLUE, "").replace(Fore.MAGENTA, "").replace(Fore.WHITE, "").replace(Fore.LIGHTBLACK_EX, "").replace(Style.BRIGHT, "").replace(Style.RESET_ALL, "")
        padding = max(0, (width - len(clean_text)) // 2)
        return " " * padding + text
    except:
        return text.center(width)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_rainbow_banner():
    """Menampilkan Banner RootSec Bot"""
    banner_art = [
        r"██████╗  ██████╗  ██████╗ ████████╗███████╗███████╗ ██████╗ ",
        r"██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔════╝██╔════╝ ",
        r"██████╔╝██║   ██║██║   ██║   ██║   ███████╗█████╗  ██║      ",
        r"██╔══██╗██║   ██║██║   ██║   ██║   ╚════██║██╔══╝  ██║      ",
        r"██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████║███████╗╚██████╗ ",
        r"╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚══════╝ ╚═════╝ ",
        r"                VERIFICATION  BOT                           "
    ]
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    
    print("\n")
    for i, line in enumerate(banner_art):
        color = colors[i % len(colors)]
        print(center_text(f"{Style.BRIGHT}{color}{line}"))
    print(center_text(f"{Fore.WHITE}Created by Toko RootSec Bot"))
    print("\n" + center_text(f"{Fore.LIGHTBLACK_EX}{'='*60}"))
    print("")

def show_tutorial():
    """Menampilkan Halaman Tutorial di Terminal"""
    clear_screen()
    print(f"\n{center_text(Fore.YELLOW + '╔════════════════════════════════════════╗')}")
    print(f"{center_text(Fore.YELLOW + '║      PANDUAN PENGGUNAAN SCRIPT         ║')}")
    print(f"{center_text(Fore.YELLOW + '╚════════════════════════════════════════╝')}\n")

    print(f"{Fore.CYAN}1. INSTALASI LIBRARY (PENTING){Style.RESET_ALL}")
    print("   Sebelum menggunakan, pastikan semua module terinstall.")
    print(f"   Ketik perintah: {Fore.GREEN}pip install -r requirements.txt{Style.RESET_ALL}\n")

    print(f"{Fore.CYAN}2. KONFIGURASI TOOL VETERANS (MENU 2){Style.RESET_ALL}")
    print("   Tool Veterans butuh setting manual agar bisa jalan:")
    print(f"   a. Masuk ke folder {Fore.MAGENTA}veterans-verify-tool/{Style.RESET_ALL}")
    print(f"   b. Ubah {Fore.WHITE}config.example.json{Style.RESET_ALL} jadi {Fore.GREEN}config.json{Style.RESET_ALL}")
    print(f"   c. Isi {Fore.YELLOW}accessToken{Style.RESET_ALL} (ambil dari https://chatgpt.com/api/auth/session)")
    print(f"   d. Isi data target di file {Fore.GREEN}data.txt{Style.RESET_ALL} (Format: Nama|Nama|Branch|Lahir|Discharge)\n")

    print(f"{Fore.CYAN}3. MENGATASI IP LIMIT / BLOKIR{Style.RESET_ALL}")
    print("   Jika verifikasi gagal terus menerus, gunakan Proxy.")
    print(f"   Buat file {Fore.GREEN}proxy.txt{Style.RESET_ALL} di dalam folder tool yang ingin dipakai.")
    print("   Format: user:pass@host:port\n")

    print(f"{Fore.CYAN}4. CARA KELUAR{Style.RESET_ALL}")
    print("   Tekan CTRL+C kapan saja untuk memaksa berhenti, atau pilih menu 0.\n")
    
    print(f"{Fore.LIGHTBLACK_EX}{'-'*60}{Style.RESET_ALL}")
    input(center_text(f"Tekan {Fore.GREEN}[ENTER]{Style.RESET_ALL} untuk kembali ke Menu Utama..."))

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

        # Loop menu tools
        for key, (name, _) in TOOLS.items():
            print(center_text(f"{Fore.CYAN}{key.center(3)} {Fore.WHITE}- {name}"))
        
        print("")
        # Menu tambahan untuk Tutorial & Exit
        print(center_text(f"{Fore.GREEN}[8]   PANDUAN / TUTORIAL{Style.RESET_ALL}"))
        print(center_text(f"{Fore.RED}[0]   KELUAR / EXIT     {Style.RESET_ALL}"))
        print("")
        print(center_text(f"{Fore.LIGHTBLACK_EX}{'='*60}"))
        
        sys.stdout.write(f"\n{Fore.GREEN}RootSec@Bot ~# {Style.RESET_ALL}")
        choice = input().strip()

        if choice == '0':
            print(f"\n{Fore.MAGENTA}Terima kasih telah menggunakan RootSec Bot. Bye!{Style.RESET_ALL}")
            sys.exit()
        
        elif choice == '8':
            show_tutorial() # Panggil fungsi tutorial
        
        elif choice in TOOLS:
            _, folder = TOOLS[choice]
            run_script(folder)
        else:
            print(f"\n{Fore.RED} [!] Pilihan salah. Masukkan angka 0-8.{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Force Close.{Style.RESET_ALL}")
        sys.exit()
