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
from utils import (
    check_and_install_dependencies, clear_screen, 
    success_message, error_message, info_message, 
    display_banner, check_for_update, display_system_info, exit_program,
    display_menu, display_tool_info
)
from auth import AuthManager

# Import tools
from tools import (
    # Passive Reconnaissance
    WhoisScraper, DNSRecordDumper, SubdomainFinder, WaybackMachineExtractor, GoogleDorkAutomator,
    # Active Reconnaissance
    PingSweepScanner, TCPSYNScanner, TracerouteTool,
    # OSINT
    EXIFDataViewer, EmailHarvester,
    # Web Application Security
    WebDirectoryBruteForcer, TechStackDetector,
    # Cryptography, Password, & Data Hiding
    HashIdentifier, HashCracker, DataEncoderDecoder,
    # Forensics, Malware Analysis, & Blue Team
    FileSignatureChecker, NetworkConnectionMonitor,
    # Utilities & Fun Projects
    SecureFileShredder, MorseCodeTranslator
)

# --- KONFIGURASI AUTENTIKASI GITHUB ---
# Ganti dengan Personal Access Token (PAT), nama pemilik repo, dan nama repo Anda.
# PAT harus memiliki izin 'repo' untuk membaca dan menulis file.
GITHUB_PAT = "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" 
REPO_OWNER = "Habibzz01"
REPO_NAME = "dbsc"
# -----------------------------------------


# Kategori tools
CATEGORIES = [
    {
        "id": 1,
        "name": "Passive Reconnaissance",
        "tools": [
            {"id": 1, "name": "Whois Scraper", "class": WhoisScraper, "desc": "ngambil data domain di whois"},
            {"id": 2, "name": "DNS Record Dumper", "class": DNSRecordDumper, "desc": "Mengekstrak semua jenis record DNS"},
            {"id": 3, "name": "Subdomain Finder", "class": SubdomainFinder, "desc": "Menemukan subdomain gunain dorking"},
            {"id": 4, "name": "Wayback Machine URL Extractor", "class": WaybackMachineExtractor, "desc": "ngambil URL yang pernah diarsipin"},
            {"id": 5, "name": "Google Dork Automator", "class": GoogleDorkAutomator, "desc": "Menjalankan dork untuk cari info sensitif"}
        ]
    },
    {
        "id": 2,
        "name": "Active Reconnaissance",
        "tools": [
            {"id": 1, "name": "Ping Sweep Scanner", "class": PingSweepScanner, "desc": "Memeriksa host aktif dalam rentang IP"},
            {"id": 2, "name": "TCP SYN Scanner", "class": TCPSYNScanner, "desc": "Memindai port terbuka tanpa handshake"},
            {"id": 3, "name": "Traceroute Tool", "class": TracerouteTool, "desc": "Memetakan jalur paket ke target"}
        ]
    },
    {
        "id": 3,
        "name": "OSINT",
        "tools": [
            {"id": 1, "name": "EXIF Data Viewer", "class": EXIFDataViewer, "desc": "Menampilkan metadata file gambar"},
            {"id": 2, "name": "Email Harvester", "class": EmailHarvester, "desc": "Mengumpulkan alamat email dari website"}
        ]
    },
    {
        "id": 4,
        "name": "Web Application Security",
        "tools": [
            {"id": 1, "name": "Web Directory Brute-forcer", "class": WebDirectoryBruteForcer, "desc": "Menebak file dan direktori umum"},
            {"id": 2, "name": "Tech Stack Detector", "class": TechStackDetector, "desc": "Mengidentifikasi teknologi website"}
        ]
    },
    {
        "id": 5,
        "name": "Intinya tentang Penyembunyian Password",
        "tools": [
            {"id": 1, "name": "Hash Identifier", "class": HashIdentifier, "desc": "Mengidentifikasi tipe hash"},
            {"id": 2, "name": "Hash Cracker", "class": HashCracker, "desc": "Memecahkan hash dengan wordlist"},
            {"id": 3, "name": "Data Encoder/Decoder", "class": DataEncoderDecoder, "desc": "Konversi data (Base64, URL, Hex)"}
        ]
    },
    {
        "id": 6,
        "name": "Forensics, Malware Analysis, & Blue Team (Andro Root)",
        "tools": [
            {"id": 1, "name": "File Signature Checker", "class": FileSignatureChecker, "desc": "Memverifikasi tipe file berdasarkan magic number"},
            {"id": 2, "name": "Network Connection Monitor", "class": NetworkConnectionMonitor, "desc": "Menampilkan koneksi jaringan aktif"}
        ]
    },
    {
        "id": 7,
        "name": "Tools Lainnyaa anjg",
        "tools": [
            {"id": 1, "name": "Secure File Shredder", "class": SecureFileShredder, "desc": "Menimpa file sebelum menghapusnya"},
            {"id": 2, "name": "Morse Code Translator", "class": MorseCodeTranslator, "desc": "Menerjemahkan teks ke kode Morse"}
        ]
    }
]

# --- Owner Tools ---
# Wrapper classes to integrate auth functions into the existing tool structure
class AddUserTool:
    def __init__(self, auth_manager): self.auth_manager = auth_manager
    def run(self): self.auth_manager.add_user(); input("\nTekan Enter untuk kembali...")
class DeleteUserTool:
    def __init__(self, auth_manager): self.auth_manager = auth_manager
    def run(self): self.auth_manager.delete_user(); input("\nTekan Enter untuk kembali...")
class ListUsersTool:
    def __init__(self, auth_manager): self.auth_manager = auth_manager
    def run(self): self.auth_manager.list_users(); input("\nTekan Enter untuk kembali...")

def get_owner_category(auth_manager):
    return {
        "id": 8,
        "name": "Owner Menu",
        "tools": [
            {"id": 1, "name": "Add User", "class": lambda: AddUserTool(auth_manager), "desc": "Menambahkan pengguna baru"},
            {"id": 2, "name": "Delete User", "class": lambda: DeleteUserTool(auth_manager), "desc": "Menghapus pengguna yang ada"},
            {"id": 3, "name": "List Users", "class": lambda: ListUsersTool(auth_manager), "desc": "Menampilkan semua pengguna"},
        ]
    }


def display_main_menu(categories_to_display):
    clear_screen()
    display_banner()
    display_system_info()
    
    menu_data = [[f"\033[94m{cat['id']:02d}\033[0m", cat["name"]] for cat in categories_to_display]
    
    headers = ["ID", "Kategori Tools"]
    print("\n" + "="*60)
    print("MENU UTAMA - PILIH KATEGORI")
    print("="*60)
    display_menu(menu_data, headers, title=None, tablefmt="rounded_outline")
    
    print("\n" + "="*60)
    print(f"[\033[91m00\033[0m] Keluar")
    print("="*60)

def display_category_menu(category):
    clear_screen()
    menu_data = [[f"\033[92m{tool['id']:02d}\033[0m", tool["name"], tool["desc"]] for tool in category["tools"]]
    
    headers = ["ID", "Nama Tool", "Deskripsi"]
    print("\n" + "="*80)
    print(f"{category['name'].upper()}")
    print("="*80)
    display_menu(menu_data, headers, title=None, tablefmt="rounded_outline")
    
    print("\n" + "="*80)
    print(f"[\033[91m00\033[0m] Kembali ke Menu Utama")
    print("="*80)

def run_tool(tool_info):
    try:
        display_tool_info(tool_info["name"], tool_info["desc"])
        tool_instance = tool_info["class"]()
        tool_instance.run()
    except Exception as e:
        error_message(f"Error menjalankan tool: {str(e)}")
        input("\nTekan Enter untuk kembali ke menu...")


def main():
    check_and_install_dependencies()
    
    try:
        auth_manager = AuthManager(GITHUB_PAT, REPO_OWNER, REPO_NAME)
    except ValueError as e:
        error_message(str(e))
        error_message("Silakan isi variabel GITHUB_PAT, REPO_OWNER, dan REPO_NAME di main.py.")
        sys.exit(1)

    username, user_role = auth_manager.login()

    if not username:
        exit_program()

    # check_for_update() # Dihapus sementara untuk fokus pada fitur login

    while True:
        current_categories = CATEGORIES.copy()
        if user_role == 'owner':
            current_categories.append(get_owner_category(auth_manager))

        display_main_menu(current_categories)
        
        try:
            choice_str = input(f"\n[?] Pilih kategori (0-{len(current_categories)}): ")
            if not choice_str.isdigit():
                error_message("Masukkan angka yang valid.")
                time.sleep(1)
                continue
            
            choice = int(choice_str)
            if choice == 0:
                exit_program()
            
            selected_category = next((cat for cat in current_categories if cat['id'] == choice), None)

            if selected_category:
                while True:
                    display_category_menu(selected_category)
                    
                    try:
                        tool_choice_str = input(f"\n[?] Pilih tool (0-{len(selected_category['tools'])}): ")
                        if not tool_choice_str.isdigit():
                             error_message("Masukkan angka yang valid.")
                             time.sleep(1)
                             continue
                        
                        tool_choice = int(tool_choice_str)
                        if tool_choice == 0:
                            break
                        
                        selected_tool = next((t for t in selected_category['tools'] if t['id'] == tool_choice), None)

                        if selected_tool:
                            run_tool(selected_tool)
                        else:
                            error_message("Pilihan tool tidak valid.")
                            time.sleep(1)
                    except ValueError:
                        error_message("Masukkan angka yang valid.")
                        time.sleep(1)
            else:
                error_message("Pilihan kategori tidak valid.")
                time.sleep(1)
        except ValueError:
            error_message("Masukkan angka yang valid.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[91m[!] Program dihentikan oleh pengguna.\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91m[!] Error tidak terduga: {str(e)}\033[0m")
        sys.exit(1)