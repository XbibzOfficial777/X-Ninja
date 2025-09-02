#!/usr/bin/env python3
# -*- coding: utf-8 -*-




#===========================================
#  Tools Created By Xbibz Official!                     
#     Do Not Recode!                         
# Youtube : https://youtube.com/@XbibzOfficial
# TikTok  : https://tiktok.com/@xbibzofficiall
#===========================================






import os
import sys
import time
import random
import subprocess
import platform
import requests
import json
from tabulate import tabulate
from datetime import datetime



# Cek dan install dependencies otomatis
def check_and_install_dependencies():
    required_packages = [
        'colorama',
        'tabulate'
    ]
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').split('.')[0])
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"[!] Mendeteksi {len(missing_packages)} packages yang belum terinstall...")
        for package in missing_packages:
            print(f"[+] Menginstall {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("[✓] Semua packages telah berhasil diinstall!")
        time.sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)

# Fungsi untuk membersihkan terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk animasi loading
def loading_animation(text="Memproses", duration=1):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start_time = time.time()
    while time.time() - start_time < duration:
        for frame in frames:
            sys.stdout.write(f"\r{frame} {text}...")
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()

# Fungsi untuk menampilkan pesan sukses
def success_message(message):
    print(f"\033[92m[✓] {message}\033[0m")

# Fungsi untuk menampilkan pesan error
def error_message(message):
    print(f"\033[91m[✗] {message}\033[0m")

# Fungsi untuk menampilkan pesan info
def info_message(message):
    print(f"\033[93m[i] {message}\033[0m")

# Fungsi untuk menampilkan pesan warning
def warning_message(message):
    print(f"\033[95m[!] {message}\033[0m")

# Fungsi untuk menampilkan banner
def display_banner():
    banner = """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⠀⠀⠀⢀⣴⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡟⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⢶⣾⣿⣿⡟⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⠟⢋⡡⠖⠉⠀⢸⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡾⠛⢉⡠⠾⢷⡉⠀⠀⠀⠀⠌⢹⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡾⠟⢁⡴⠚⠁⠀⠀⢀⣽⠿⣄⡀⠰⠀⣿⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠋⢀⠔⠁⠀⠀⠀⢀⣴⡿⠋⠀⠀⠈⠉⠛⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠄⠊⢙⣇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠏⢀⡔⠁⠀⠀⠀⢀⣴⣿⡟⠁⠀⠀⠀⠀⠀⢠⡇⠀⠀⠀Tiktok : @xbibzofficiall
⠀⠀⠀⠀⠀⠀⢀⠔⠊⠀⠀⠀⣏⢋⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠃⣠⠋⠀⠀⠀⠀⣴⣿⣿⠏⠀⠀⠀⠀⠀⢀⣄⡼⠀⠀⠀⠀YT     : @XbibzOfficial
⠀⠀⠀⠀⠀⠔⠁⠀⠀⠀⠀⠀⠈⠻⠯⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⢁⡼⠁⢀⣴⡶⠿⣿⣿⡿⠃⠀⠀⠀⠀⠀⣠⣾⣿⠃⠀⠀⠀⠀Github : XbibzOfficial777
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⢡⠞⠀⢠⣿⠋⠀⠀⠈⣿⡇⠀⠀⠀⠀⢀⣼⡿⣱⠃⠀⠀⠀⠀⠀Version: v1.0
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣷⠋⠀⠀⠘⣿⣦⣀⣀⣠⣿⠃⠀⠀⠀⣴⣿⣿⣵⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⣿⡃⠀⠀⠀⢠⣿⡿⠾⠛⠋⠁⠀⠀⣠⣾⣿⣿⣟⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡋⣻⣄⠀⢰⠿⠋⠀⠀⠀⠀⠀⣠⣾⣿⣿⡿⠋⠘⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⢤⣀⠀⣿⢦⣼⡿⣇⢱⡃⠈⢳⣄⡀⠀⠀⠀⠀⢀⣴⣿⣿⡿⠋⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣱⠤⠞⣻⣿⣶⣿⡇⠘⢯⢙⡦⣏⠀⢉⡷⠦⢤⣴⣿⣟⡿⠋⠀⠀⠀⠀⠀⠸⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠿⢯⣉⣹⠟⠁⢀⣾⣿⣿⣿⣇⢳⣤⣄⠙⠧⣄⣹⠯⣤⢴⣯⣾⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠁⠀⠀⣼⣿⣿⣻⣿⡿⠛⢩⡟⢦⣀⣀⣩⣽⣿⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠃⠀⠀⣴⣿⠏⠀⣼⠟⠀⢠⣾⣿⣷⣾⣿⣿⡯⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀
⢀⠀⠀⠀⠀⠀⠀⢠⠟⡟⠀⢀⡎⠘⠟⠀⣼⠏⢀⣴⡿⠿⢻⣹⣯⣿⣿⣿⡚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀
⠈⡄⠀⠀⠀⠀⢰⣯⣴⡇⠀⡸⠀⠀⠀⣼⣏⣴⠿⠉⠀⣀⣼⣿⣿⡿⠃⣯⡙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⡄⠀⠀⠀⠀⠀⢸⠀⢀⡇⠀⠀⣸⣛⠟⠉⠠⠶⠿⢿⠟⠋⠁⠀⣸⡇⠉⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⢠⡅⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⢄⠀⠀⠀⢠⡟⠀⣸⠀⠀⠀⠛⠁⠀⠀⠀⢀⡴⠋⠀⠀⢀⣴⡁⢷⠀⠀⠀⠀⠀⠠⢦⣄⡤⢤⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠣⡀⠀⣾⡇⢠⠇⠀⠀⠀⠀⠀⢀⡠⠖⠉⠀⢀⡠⣶⠋⠀⢳⣼⠀⠀⠀⠀⠀⠀⠀⠀⢀⠜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠢⣼⠁⡞⠀⠀⠀⣀⠤⠚⠉⢀⣠⠴⢺⣉⡼⠃⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⢀⠴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣜⡸⠁⢀⠴⠊⣁⣤⣶⠟⠉⠀⠀⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⡿⢁⣔⡥⠖⠻⢍⣉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⡷⠛⠁⠀⠀⠀⠀⠀⠉⠉⠒⠒⠒⠒⠒⠒⠒⠂⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """
    # Animasi warna untuk banner
    colors = [91, 92, 93, 94, 95, 96]
    for line in banner.split('\n'):
        color = random.choice(colors)
        print(f"\033[{color}m{line}\033[0m")
        time.sleep(0.05)

# Fungsi untuk mengecek update
def check_for_update():
    try:
        current_version = "1.1.0"
        repo_url = "https://raw.githubusercontent.com/XbibzOfficial/Termux-Multi-Tool/main/version.json"
        response = requests.get(repo_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("version", current_version)
            if latest_version > current_version:
                info_message(f"Update tersedia! Versi terbaru: {latest_version}")
                choice = input("[?] Apakah Anda ingin mengupdate sekarang? (y/n): ").lower()
                if choice == 'y':
                    info_message("Mengupdate script...")
                    # Implementasi update script
                    success_message("Update berhasil!")
                    time.sleep(2)
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                else:
                    info_message("Update ditunda.")
            else:
                success_message("Anda menggunakan versi terbaru!")
        else:
            error_message("Gagal mengecek update. Melanjutkan dengan versi saat ini.")
    except Exception as e:
        error_message(f"Error saat mengecek update: {str(e)}")

# Fungsi untuk validasi input
def validate_input(prompt, input_type=str, default=None, validation_func=None):
    while True:
        try:
            user_input = input(prompt)
            if not user_input and default is not None:
                return default
            converted_input = input_type(user_input)
            if validation_func and not validation_func(converted_input):
                error_message("Input tidak valid. Silakan coba lagi.")
                continue
            return converted_input
        except ValueError:
            error_message("Input tidak valid. Silakan coba lagi.")

# Fungsi untuk menyimpan konfigurasi
def save_config(config_data, config_file="config.json"):
    try:
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=4)
        success_message(f"Konfigurasi disimpan ke {config_file}")
    except Exception as e:
        error_message(f"Gagal menyimpan konfigurasi: {str(e)}")

# Fungsi untuk memuat konfigurasi
def load_config(config_file="config.json"):
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        error_message(f"Gagal memuat konfigurasi: {str(e)}")
        return {}

# Fungsi untuk mengecek koneksi internet
def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False

# Fungsi untuk mendapatkan IP publik
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        if response.status_code == 200:
            return response.json().get("ip", "Unknown")
        return "Unknown"
    except:
        return "Unknown"

# Fungsi untuk menampilkan informasi sistem
def display_system_info():
    print("\n" + "="*60)
    info_message("Informasi Sistem:")
    print(f"  Sistem Operasi: {platform.system()} {platform.release()}")
    print(f"  Versi Python: {platform.python_version()}")
    print(f"  Arsitektur: {platform.machine()}")
    print(f"  Hostname: {platform.node()}")
    print(f"  IP Publik: {get_public_ip()}")
    print(f"  Waktu Sekarang: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

# Fungsi untuk keluar dari program
def exit_program():
    info_message("Terima kasih telah menggunakan Xbibz Official - MR. Nexo444 Multi-Tool!")
    time.sleep(1)
    sys.exit(0)

# Fungsi untuk menampilkan menu dengan tabulate
def display_menu(data, headers, title=None, tablefmt="rounded_outline"):
    """
    Menampilkan menu dalam bentuk tabel menggunakan tabulate
    
    Args:
         List of lists berisi data menu
        headers: List berisi nama kolom
        title: Judul menu (opsional)
        tablefmt: Format tabel (default: "rounded_outline")
    """
    if title:
        print(f"\n\033[94m{title}\033[0m")
        print("=" * len(title))
    
    print(tabulate(data, headers=headers, tablefmt=tablefmt, numalign="left"))

# Fungsi untuk menampilkan informasi tool
def display_tool_info(name, description):
    """Menampilkan informasi tool yang dipilih"""
    clear_screen()
    print("\n" + "="*60)
    print(f"\033[94m{name}\033[0m")
    print("="*60)
    print(f"{description}")
    print("="*60 + "\n")

# Fungsi untuk menampilkan hasil dalam tabel
def display_result_table(data, headers, title=None, tablefmt="rounded_outline"):
    """
    Menampilkan hasil dalam bentuk tabel menggunakan tabulate
    
    Args:
         List of lists berisi data hasil
        headers: List berisi nama kolom
        title: Judul tabel (opsional)
        tablefmt: Format tabel (default: "rounded_outline")
    """
    if title:
        print(f"\n\033[94m{title}\033[0m")
        print("=" * len(title))
    
    print(tabulate(data, headers=headers, tablefmt=tablefmt, numalign="left"))

# Fungsi untuk menampilkan progress bar
def display_progress(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Menampilkan progress bar
    
    Args:
        iteration: Iterasi saat ini
        total: Total iterasi
        prefix: Teks sebelum progress bar
        suffix: Teks setelah progress bar
        decimals: Jumlah desimal pada persentase
        length: Panjang progress bar
        fill: Karakter untuk mengisi progress bar
        print_end: Karakter akhir untuk print
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print new line on complete
    if iteration == total: 
        print()