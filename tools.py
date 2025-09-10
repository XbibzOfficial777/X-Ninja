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
import json
import socket
import requests
import whois
import dns.resolver
import subprocess
import threading
import queue
import ipaddress
import re
import base64
import hashlib
import ssl
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup
from utils import (
    clear_screen, loading_animation, success_message, error_message, 
    info_message, warning_message, validate_input, check_internet_connection,
    display_progress, display_result_table
)
from concurrent.futures import ThreadPoolExecutor, as_completed

# KATEGORI I: PASSIVE RECONNAISSANCE (PASIF)
class WhoisScraper:
    def __init__(self):
        self.name = "Whois Scraper"
        self.description = "Mengambil data Whois sebuah domain secara otomatis"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        if not check_internet_connection():
            error_message("Tidak ada koneksi internet!")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        domain = validate_input("[?] Masukkan domain: ", str)
        try:
            print(f"\nMengambil data Whois untuk {domain}...")
            w = whois.whois(domain)
            
            # Siapkan data untuk tabel
            results = []
            for key, value in w.items():
                if value and key not in ['raw', 'text']:
                    if isinstance(value, list):
                        value = ", ".join(str(v) for v in value)
                    results.append([key, str(value)])
            
            # Tampilkan hasil dalam tabel
            if results:
                headers = ["Field", "Value"]
                display_result_table(results, headers, title=f"Hasil Whois untuk {domain}", tablefmt="rounded_outline")
                success_message("Data Whois berhasil diambil!")
            else:
                warning_message("Tidak ada data Whois yang ditemukan!")
            
            # Simpan hasil ke file
            with open(f"{domain}_whois.txt", "w") as f:
                for key, value in w.items():
                    if value:
                        f.write(f"{key}: {value}\n")
            success_message(f"Data Whois disimpan ke {domain}_whois.txt")
            
        except Exception as e:
            error_message(f"Gagal mengambil data Whois: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

class DNSRecordDumper:
    def __init__(self):
        self.name = "DNS Record Dumper"
        self.description = "Mengekstrak semua jenis record DNS (A, AAAA, MX, TXT, NS)"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        if not check_internet_connection():
            error_message("Tidak ada koneksi internet!")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        domain = validate_input("[?] Masukkan domain: ", str)
        record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA', 'PTR', 'SRV']
        
        try:
            print(f"\nMengekstrak record DNS untuk {domain}...")
            results = []
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    for rdata in answers:
                        results.append([record_type, str(rdata)])
                except Exception as e:
                    # Skip jika record tidak ditemukan
                    pass
            
            # Tampilkan hasil dalam tabel
            if results:
                headers = ["Record Type", "Value"]
                display_result_table(results, headers, title=f"DNS Records untuk {domain}", tablefmt="rounded_outline")
                success_message("Record DNS berhasil diekstrak!")
                
                # Simpan hasil ke file
                with open(f"{domain}_dns_records.txt", "w") as f:
                    f.write(f"DNS Records untuk {domain}\n")
                    f.write("="*50 + "\n")
                    for record_type, value in results:
                        f.write(f"{record_type}: {value}\n")
                success_message(f"Record DNS disimpan ke {domain}_dns_records.txt")
            else:
                warning_message("Tidak ada record DNS yang ditemukan!")
                
        except Exception as e:
            error_message(f"Gagal mengekstrak record DNS: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

class SubdomainFinder:
    def __init__(self):
        self.name = "Subdomain Finder"
        self.description = "Menggunakan dorking Google/Bing untuk menemukan subdomain"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        if not check_internet_connection():
            error_message("Tidak ada koneksi internet!")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        domain = validate_input("[?] Masukkan domain: ", str)
        # Daftar dork untuk mencari subdomain
        dorks = [
            f"site:*.{domain}",
            f"site:{domain} -www",
            f"site:{domain} inurl:admin",
            f"site:{domain} inurl:login",
            f"site:{domain} inurl:wp-admin",
            f"site:{domain} inurl:cpanel",
            f"site:{domain} inurl:dev",
            f"site:{domain} inurl:test",
            f"site:{domain} inurl:staging",
            f"site:{domain} inurl:api"
        ]
        
        subdomains = set()
        
        try:
            print(f"\nMencari subdomain untuk {domain}...")
            
            # Gunakan ThreadPoolExecutor untuk performa lebih baik
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for dork in dorks:
                    futures.append(executor.submit(self._search_dork, dork, domain))
                
                for future in as_completed(futures):
                    subdomains.update(future.result())
            
            # Filter subdomain yang valid
            valid_subdomains = [sub for sub in subdomains if domain in sub]
            
            if valid_subdomains:
                print(f"\nDitemukan {len(valid_subdomains)} subdomain:")
                
                # Tampilkan hasil dalam tabel
                results = [[sub] for sub in sorted(valid_subdomains)[:20]]  # Tampilkan 20 pertama
                headers = ["Subdomain"]
                display_result_table(results, headers, title=f"Subdomain untuk {domain} (20 pertama)", tablefmt="rounded_outline")
                
                if len(valid_subdomains) > 20:
                    print(f"  ... dan {len(valid_subdomains) - 20} subdomain lainnya")
                
                # Simpan hasil ke file
                with open(f"{domain}_subdomains.txt", "w") as f:
                    for sub in sorted(valid_subdomains):
                        f.write(f"{sub}\n")
                success_message(f"Subdomain disimpan ke {domain}_subdomains.txt")
            else:
                warning_message("Tidak ada subdomain yang ditemukan!")
                
        except Exception as e:
            error_message(f"Gagal mencari subdomain: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def _search_dork(self, dork, domain):
        """Fungsi helper untuk mencari subdomain menggunakan dork tertentu"""
        subdomains = set()
        try:
            # Menggunakan Bing karena lebih mudah di-scrape
            url = f"https://www.bing.com/search?q={urllib.parse.quote(dork)}&count=50"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    # Ekstrak subdomain dari URL
                    if domain in href:
                        parsed = urllib.parse.urlparse(href)
                        hostname = parsed.netloc
                        if hostname and hostname != domain:
                            subdomains.add(hostname)
        except Exception as e:
            pass
        return subdomains

class WaybackMachineExtractor:
    def __init__(self):
        self.name = "Wayback Machine URL Extractor"
        self.description = "Mengambil semua URL yang pernah diarsipkan dari sebuah domain"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        if not check_internet_connection():
            error_message("Tidak ada koneksi internet!")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        domain = validate_input("[?] Masukkan domain: ", str)
        
        try:
            print(f"\nMengambil URL dari Wayback Machine untuk {domain}...")
            # API Wayback Machine
            url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&fl=original&collapse=urlkey"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1:  # Data pertama adalah header
                    urls = set()
                    for item in data[1:]:  # Skip header
                        if item and len(item) > 0:
                            urls.add(item[0])
                    
                    if urls:
                        print(f"Ditemukan {len(urls)} URL:")
                        
                        # Tampilkan hasil dalam tabel
                        results = [[url] for url in sorted(urls)[:20]]  # Tampilkan 20 pertama
                        headers = ["URL"]
                        display_result_table(results, headers, title=f"URL dari Wayback Machine untuk {domain} (20 pertama)", tablefmt="rounded_outline")
                        
                        if len(urls) > 20:
                            print(f"  ... dan {len(urls) - 20} URL lainnya")
                        
                        # Simpan hasil ke file
                        with open(f"{domain}_wayback_urls.txt", "w") as f:
                            for url in sorted(urls):
                                f.write(f"{url}\n")
                        success_message(f"URL disimpan ke {domain}_wayback_urls.txt")
                    else:
                        warning_message("Tidak ada URL yang ditemukan!")
                else:
                    warning_message("Tidak ada URL yang ditemukan!")
            else:
                error_message("Gagal mengambil data dari Wayback Machine!")
                
        except Exception as e:
            error_message(f"Gagal mengambil URL dari Wayback Machine: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

class GoogleDorkAutomator:
    def __init__(self):
        self.name = "Google Dork Automator"
        self.description = "Menjalankan berbagai dork secara otomatis untuk mencari informasi sensitif"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        if not check_internet_connection():
            error_message("Tidak ada koneksi internet!")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        domain = validate_input("[?] Masukkan domain: ", str)
        # Daftar dork untuk mencari informasi sensitif
        dorks = [
            f"site:{domain} ext:php",
            f"site:{domain} ext:asp",
            f"site:{domain} ext:jsp",
            f"site:{domain} ext:html",
            f"site:{domain} ext:txt",
            f"site:{domain} ext:log",
            f"site:{domain} ext:conf",
            f"site:{domain} ext:bak",
            f"site:{domain} ext:backup",
            f"site:{domain} ext:sql",
            f"site:{domain} ext:db",
            f"site:{domain} ext:xml",
            f"site:{domain} ext:json",
            f"site:{domain} inurl:admin",
            f"site:{domain} inurl:login",
            f"site:{domain} inurl:wp-admin",
            f"site:{domain} inurl:cpanel",
            f"site:{domain} inurl:config",
            f"site:{domain} intitle:index.of",
            f"site:{domain} intext:password",
            f"site:{domain} intext:username",
            f"site:{domain} inurl:phpmyadmin",
            f"site:{domain} inurl:.env",
            f"site:{domain} ext:pdf intitle:confidential",
            f"site:{domain} ext:doc intitle:confidential",
            f"site:{domain} ext:docx intitle:confidential"
        ]
        
        results = []
        
        try:
            print(f"\nMenjalankan Google Dork untuk {domain}...")
            
            # Gunakan ThreadPoolExecutor untuk performa lebih baik
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for dork in dorks:
                    futures.append(executor.submit(self._search_dork, dork, domain))
                
                for future in as_completed(futures):
                    results.extend(future.result())
            
            if results:
                print(f"Ditemukan {len(results)} hasil:")
                
                # Kelompokkan berdasarkan dork
                dork_results = {}
                for dork, url in results:
                    if dork not in dork_results:
                        dork_results[dork] = []
                    dork_results[dork].append(url)
                
                # Tampilkan hasil dalam tabel
                all_results = []
                for dork, urls in dork_results.items():
                    for url in urls[:3]:  # Tampilkan maksimal 3 URL per dork
                        all_results.append([dork, url])
                
                headers = ["Dork", "URL"]
                display_result_table(all_results, headers, title=f"Hasil Google Dork untuk {domain}", tablefmt="rounded_outline")
                
                # Simpan hasil ke file
                with open(f"{domain}_dork_results.txt", "w") as f:
                    for dork, urls in dork_results.items():
                        f.write(f"Dork: {dork}\n")
                        for url in urls:
                            f.write(f"  {url}\n")
                        f.write("\n")
                success_message(f"Hasil dork disimpan ke {domain}_dork_results.txt")
            else:
                warning_message("Tidak ada hasil yang ditemukan!")
                
        except Exception as e:
            error_message(f"Gagal menjalankan Google Dork: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def _search_dork(self, dork, domain):
        """Fungsi helper untuk mencari hasil dork tertentu"""
        results = []
        try:
            # Menggunakan Bing karena lebih mudah di-scrape
            url = f"https://www.bing.com/search?q={urllib.parse.quote(dork)}&count=10"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    # Filter hasil yang valid
                    if domain in href and href.startswith("http"):
                        results.append((dork, href))
        except Exception as e:
            pass
        return results

# KATEGORI II: ACTIVE RECONNAISSANCE (AKTIF)
class PingSweepScanner:
    def __init__(self):
        self.name = "Ping Sweep Scanner"
        self.description = "Memeriksa host yang aktif dalam sebuah rentang IP menggunakan ICMP"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        ip_range = validate_input("[?] Masukkan rentang IP (contoh: 192.168.1.0/24): ", str)
        
        try:
            network = ipaddress.ip_network(ip_range, strict=False)
            hosts_up = []
            total_hosts = network.num_addresses
            
            print(f"\nMemindai {total_hosts} host dalam {ip_range}...")
            
            # Gunakan ThreadPoolExecutor untuk performa lebih baik
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {}
                for ip in network.hosts():
                    future = executor.submit(self._ping_host, str(ip))
                    futures[future] = str(ip)
                
                completed = 0
                for future in as_completed(futures):
                    ip = futures[future]
                    is_up = future.result()
                    completed += 1
                    
                    # Tampilkan progress
                    display_progress(completed, total_hosts, prefix='Progress:', suffix='Complete', length=50)
                    
                    if is_up:
                        hosts_up.append(ip)
            
            # Tampilkan hasil dalam tabel
            if hosts_up:
                print(f"\nDitemukan {len(hosts_up)} host aktif:")
                
                results = [[ip] for ip in sorted(hosts_up)]
                headers = ["IP Address"]
                display_result_table(results, headers, title=f"Host Aktif dalam {ip_range}", tablefmt="rounded_outline")
                
                # Simpan hasil ke file
                with open(f"ping_sweep_{ip_range.replace('/', '_')}.txt", "w") as f:
                    for ip in sorted(hosts_up):
                        f.write(f"{ip}\n")
                success_message(f"Hasil ping sweep disimpan ke ping_sweep_{ip_range.replace('/', '_')}.txt")
            else:
                warning_message("Tidak ada host aktif yang ditemukan!")
                
        except Exception as e:
            error_message(f"Gagal melakukan ping sweep: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def _ping_host(self, ip):
        """Fungsi helper untuk memeriksa apakah host aktif"""
        try:
            # Parameter ping berbeda untuk Windows dan Linux
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            response = subprocess.run(['ping', param, '1', '-w', '500', ip], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return response.returncode == 0
        except:
            return False

class TCPSYNScanner:
    def __init__(self):
        self.name = "TCP SYN Scanner"
        self.description = "Memindai port terbuka tanpa menyelesaikan koneksi 3-way handshake"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        target = validate_input("[?] Masukkan target IP: ", str)
        
        try:
            # Validasi IP
            ipaddress.ip_address(target)
            # Port umum yang akan di-scan
            common_ports = [
                21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995,
                1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 8888
            ]
            
            open_ports = []
            total_ports = len(common_ports)
            
            print(f"\nMemindai {total_ports} port umum di {target}...")
            
            # Gunakan ThreadPoolExecutor untuk performa lebih baik
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {}
                for port in common_ports:
                    future = executor.submit(self._scan_port, target, port)
                    futures[future] = port
                
                completed = 0
                for future in as_completed(futures):
                    port = futures[future]
                    is_open, service = future.result()
                    completed += 1
                    
                    # Tampilkan progress
                    display_progress(completed, total_ports, prefix='Progress:', suffix='Complete', length=50)
                    
                    if is_open:
                        open_ports.append((port, service))
            
            # Tampilkan hasil dalam tabel
            if open_ports:
                print(f"\nDitemukan {len(open_ports)} port terbuka:")
                
                results = [[port, service] for port, service in sorted(open_ports)]
                headers = ["Port", "Service"]
                display_result_table(results, headers, title=f"Port Terbuka di {target}", tablefmt="rounded_outline")
                
                # Simpan hasil ke file
                with open(f"tcp_scan_{target}.txt", "w") as f:
                    for port, service in sorted(open_ports):
                        f.write(f"{port}/{service}\n")
                success_message(f"Hasil scan disimpan ke tcp_scan_{target}.txt")
            else:
                warning_message("Tidak ada port terbuka yang ditemukan!")
                
        except Exception as e:
            error_message(f"Gagal memindai port: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def _scan_port(self, target, port):
        """Fungsi helper untuk memindai satu port"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target, port))
            s.close()
            
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                return True, service
            return False, None
        except:
            return False, None

class TracerouteTool:
    def __init__(self):
        self.name = "Traceroute Tool"
        self.description = "Memetakan jalur paket dari Anda ke target"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        target = validate_input("[?] Masukkan target (domain atau IP): ", str)
        
        try:
            # Parameter traceroute berbeda untuk Windows dan Linux
            if platform.system().lower() == 'windows':
                command = ['tracert', target]
            else:
                command = ['traceroute', target]
            
            print(f"\nMelakukan traceroute ke {target}...")
            response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if response.returncode == 0:
                # Parse hasil traceroute
                lines = response.stdout.split('\n')
                results = []
                for line in lines[2:]:  # Lewati 2 baris pertama
                    if line.strip() and not line.startswith('Tracing') and not line.startswith('traceroute'):
                        parts = re.split(r'\s+', line.strip())
                        if len(parts) > 1 and re.match(r'\d+', parts[0]):
                            hop = parts[0]
                            ips = [p for p in parts[1:] if re.match(r'\d+\.\d+\.\d+\.\d+', p)]
                            hostnames = [p for p in parts[1:] if not re.match(r'\d+\.\d+\.\d+\.\d+', p) and p != '*']
                            results.append([hop, ", ".join(ips), ", ".join(hostnames)])
                
                # Tampilkan hasil dalam tabel
                if results:
                    headers = ["Hop", "IP Address", "Hostname"]
                    display_result_table(results, headers, title=f"Hasil Traceroute ke {target}", tablefmt="rounded_outline")
                else:
                    print(response.stdout)
                
                # Simpan hasil ke file
                with open(f"traceroute_{target}.txt", "w") as f:
                    f.write(response.stdout)
                success_message(f"Hasil traceroute disimpan ke traceroute_{target}.txt")
            else:
                error_message(f"Gagal melakukan traceroute: {response.stderr}")
                
        except Exception as e:
            error_message(f"Gagal melakukan traceroute: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

# KATEGORI III: OSINT (OPEN-SOURCE INTELLIGENCE)
class EXIFDataViewer:
    def __init__(self):
        self.name = "EXIF Data Viewer"
        self.description = "Menampilkan semua metadata dari sebuah file gambar"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        image_path = validate_input("[?] Masukkan path ke file gambar: ", str)
        if not os.path.exists(image_path):
            error_message(f"File tidak ditemukan: {image_path}")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        try:
            # Coba install Pillow jika belum terinstall
            try:
                from PIL import Image
                from PIL.ExifTags import TAGS
            except ImportError:
                info_message("Menginstall Pillow untuk melihat EXIF data...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
                from PIL import Image
                from PIL.ExifTags import TAGS
            
            print(f"\nMembaca EXIF data dari {image_path}...")
            image = Image.open(image_path)
            # Dapatkan EXIF data
            exif_data = image._getexif()
            
            if exif:
                # Siapkan data untuk tabel
                results = []
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    results.append([tag, str(value)])
                
                # Tampilkan hasil dalam tabel
                headers = ["Tag", "Value"]
                display_result_table(results, headers, title=f"EXIF Data untuk {os.path.basename(image_path)}", tablefmt="rounded_outline")
                success_message("EXIF data berhasil dibaca!")
            else:
                warning_message("Tidak ada EXIF data yang ditemukan!")
                
        except Exception as e:
            error_message(f"Gagal membaca EXIF  {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

class EmailHarvester:
    def __init__(self):
        self.name = "Email Harvester"
        self.description = "Mengumpulkan alamat email dari website target"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        if not check_internet_connection():
            error_message("Tidak ada koneksi internet!")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        url = validate_input("[?] Masukkan URL website: ", str)
        # Pastikan URL memiliki protokol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            print(f"\nMengumpulkan email dari {url}...")
            response = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }, timeout=15)
            
            if response.status_code == 200:
                # Regex untuk mencari email
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, response.text)
                # Hapus duplikat
                unique_emails = list(set(emails))
                
                if unique_emails:
                    print(f"Ditemukan {len(unique_emails)} email:")
                    
                    # Tampilkan hasil dalam tabel
                    results = [[email] for email in sorted(unique_emails)]
                    headers = ["Email"]
                    display_result_table(results, headers, title=f"Email dari {url}", tablefmt="rounded_outline")
                    
                    # Simpan hasil ke file
                    filename = f"emails_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.txt"
                    with open(filename, "w") as f:
                        for email in sorted(unique_emails):
                            f.write(f"{email}\n")
                    success_message(f"Email disimpan ke {filename}")
                else:
                    warning_message("Tidak ada email yang ditemukan!")
            else:
                error_message(f"Gagal mengakses website: Status code {response.status_code}")
                
        except Exception as e:
            error_message(f"Gagal mengumpulkan email: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

# KATEGORI IV: WEB APPLICATION SECURITY
class WebDirectoryBruteForcer:
    def __init__(self):
        self.name = "Web Directory Brute-forcer"
        self.description = "Menebak file dan direktori umum (/admin, /config.php)"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        if not check_internet_connection():
            error_message("Tidak ada koneksi internet!")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        url = validate_input("[?] Masukkan URL website: ", str)
        # Pastikan URL memiliki protokol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        # Hapus trailing slash
        if url.endswith('/'):
            url = url[:-1]
        
        try:
            # Daftar direktori dan file umum
            common_paths = [
                '/admin', '/login', '/wp-admin', '/wp-login.php', '/administrator',
                '/config', '/config.php', '/configuration', '/setup', '/install',
                '/test', '/dev', '/staging', '/backup', '/backups', '/old',
                '/tmp', '/temp', '/private', '/protected', '/secure',
                '/robots.txt', '/sitemap.xml', '/crossdomain.xml', '/.htaccess',
                '/.env', '/.git', '/.svn', '/.DS_Store', '/web.config',
                '/phpinfo.php', '/info.php', '/test.php', '/index.php~',
                '/index.php.bak', '/index.php.old', '/index.php.backup',
                '/admin.php', '/admin.html', '/admin.asp', '/admin.aspx',
                '/console', '/controlpanel', '/cpanel', '/panel', '/manage',
                '/dashboard', '/myaccount', '/account', '/user', '/users',
                '/api', '/api/v1', '/api/v2', '/rest', '/graphql', '/graphql/v1',
                '/uploads', '/upload', '/files', '/images', '/img', '/media',
                '/js', '/css', '/assets', '/static', '/resources', '/content',
                '/includes', '/inc', '/lib', '/library', '/vendor', '/node_modules',
                '/db', '/database', '/sql', '/mysql', '/backup', '/backup.sql',
                '/dump', '/export', '/import', '/data', '/docs', '/documentation'
            ]
            
            found_paths = []
            total_paths = len(common_paths)
            
            print(f"\nMemeriksa {total_paths} path umum di {url}...")
            
            # Gunakan ThreadPoolExecutor untuk performa lebih baik
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {}
                for path in common_paths:
                    future = executor.submit(self._check_path, url, path)
                    futures[future] = path
                
                completed = 0
                for future in as_completed(futures):
                    path = futures[future]
                    result = future.result()
                    completed += 1
                    
                    # Tampilkan progress
                    display_progress(completed, total_paths, prefix='Progress:', suffix='Complete', length=50)
                    
                    if result:
                        found_paths.append(result)
            
            # Tampilkan hasil dalam tabel
            if found_paths:
                print(f"\nDitemukan {len(found_paths)} path:")
                
                results = [[path, str(status), str(size)] for path, status, size in sorted(found_paths)]
                headers = ["Path", "Status", "Size (bytes)"]
                display_result_table(results, headers, title=f"Path Terbuka di {url}", tablefmt="rounded_outline")
                
                # Simpan hasil ke file
                filename = f"dirbuster_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.txt"
                with open(filename, "w") as f:
                    for path, status, size in sorted(found_paths):
                        f.write(f"{path} - Status: {status}, Size: {size} bytes\n")
                success_message(f"Hasil brute force disimpan ke {filename}")
            else:
                warning_message("Tidak ada path yang ditemukan!")
                
        except Exception as e:
            error_message(f"Gagal melakukan brute force: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")
    
    def _check_path(self, url, path):
        """Fungsi helper untuk memeriksa satu path"""
        try:
            full_url = url + path
            response = requests.get(full_url, timeout=5, 
                                  headers={
                                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                  })
            if response.status_code == 200:
                size = len(response.content)
                return (path, response.status_code, size)
            return None
        except:
            return None

class TechStackDetector:
    def __init__(self):
        self.name = "Tech Stack Detector"
        self.description = "Mengidentifikasi framework, CMS, dan library yang digunakan (Wappalyzer clone)"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        if not check_internet_connection():
            error_message("Tidak ada koneksi internet!")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        url = validate_input("[?] Masukkan URL website: ", str)
        # Pastikan URL memiliki protokol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            print(f"\nMendeteksi teknologi di {url}...")
            response = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                headers = response.headers
                # Deteksi berdasarkan header
                detected_tech = []
                
                # Server
                if 'Server' in headers:
                    server = headers['Server']
                    if 'Apache' in server:
                        detected_tech.append(('Web Server', 'Apache'))
                    elif 'nginx' in server:
                        detected_tech.append(('Web Server', 'Nginx'))
                    elif 'IIS' in server:
                        detected_tech.append(('Web Server', 'IIS'))
                    else:
                        detected_tech.append(('Web Server', server))
                
                # X-Powered-By
                if 'X-Powered-By' in headers:
                    powered_by = headers['X-Powered-By']
                    if 'PHP' in powered_by:
                        detected_tech.append(('Programming Language', 'PHP'))
                    elif 'ASP.NET' in powered_by:
                        detected_tech.append(('Framework', 'ASP.NET'))
                    else:
                        detected_tech.append(('Technology', powered_by))
                
                # Deteksi berdasarkan meta tag
                meta_generator = re.search(r'<meta\s+name="generator"\s+content="([^"]*)"', html, re.IGNORECASE)
                if meta_generator:
                    generator = meta_generator.group(1).lower()
                    if 'wordpress' in generator:
                        detected_tech.append(('CMS', 'WordPress'))
                    elif 'joomla' in generator:
                        detected_tech.append(('CMS', 'Joomla'))
                    elif 'drupal' in generator:
                        detected_tech.append(('CMS', 'Drupal'))
                    else:
                        detected_tech.append(('Generator', generator))
                
                # Deteksi berdasarkan konten HTML
                if 'wp-content' in html:
                    detected_tech.append(('CMS', 'WordPress'))
                elif '/joomla/' in html:
                    detected_tech.append(('CMS', 'Joomla'))
                elif '/sites/default/files/' in html:
                    detected_tech.append(('CMS', 'Drupal'))
                
                # Deteksi JavaScript libraries
                if 'jquery' in html.lower():
                    detected_tech.append(('JavaScript Library', 'jQuery'))
                if 'bootstrap' in html.lower():
                    detected_tech.append(('CSS Framework', 'Bootstrap'))
                if 'react' in html.lower():
                    detected_tech.append(('JavaScript Framework', 'React'))
                if 'angular' in html.lower():
                    detected_tech.append(('JavaScript Framework', 'Angular'))
                if 'vue' in html.lower():
                    detected_tech.append(('JavaScript Framework', 'Vue.js'))
                
                # Deteksi berdasarkan URL
                if '/wp-admin' in html or '/wp-login.php' in html:
                    detected_tech.append(('CMS', 'WordPress'))
                elif '/administrator' in html:
                    detected_tech.append(('CMS', 'Joomla'))
                
                # Tampilkan hasil dalam tabel
                if detected_tech:
                    results = [[category, tech] for category, tech in detected_tech]
                    headers = ["Kategori ny mek", "Teknologi"]
                    display_result_table(results, headers, title=f"Teknologi Terdeteksi di {url}", tablefmt="rounded_outline")
                    
                    # Simpan hasil ke file
                    filename = f"tech_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.txt"
                    with open(filename, "w") as f:
                        for category, tech in detected_tech:
                            f.write(f"{category}: {tech}\n")
                    success_message(f"Hasil deteksi disimpan ke {filename}")
                else:
                    warning_message("Tidak ada teknologi yang terdeteksi!")
            else:
                error_message(f"Gagal mengakses website: Status code {response.status_code}")
                
        except Exception as e:
            error_message(f"Gagal mendeteksi teknologi: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

# V: CRYPTOGRAPHY, PASSWORD, & DATA HIDING
class HashIdentifier:
    def __init__(self):
        self.name = "Hash Identifier"
        self.description = "Mengidentifikasi tipe hash"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        hash_value = validate_input("[?] Masukkan hash: ", str)
        # Pola untuk berbagai jenis hash
        hash_patterns = {
            'MD5': r'^[a-f0-9]{32}$',
            'SHA-1': r'^[a-f0-9]{40}$',
            'SHA-256': r'^[a-f0-9]{64}$',
            'SHA-512': r'^[a-f0-9]{128}$',
            'NTLM': r'^[a-f0-9]{32}$',
            'MySQL': r'^\*[a-f0-9]{40}$',
            'Base64': r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$',
            'Hex': r'^[a-f0-9]+$'
        }
        
        possible_hashes = []
        for hash_type, pattern in hash_patterns.items():
            if re.match(pattern, hash_value, re.IGNORECASE):
                possible_hashes.append([hash_type])
        
        if possible_hashes:
            print(f"\nHash mungkin bertipe:")
            
            # Tampilkan hasil dalam tabel
            headers = ["Tipe Hash"]
            display_result_table(possible_hashes, headers, title="Identifikasi Hash", tablefmt="rounded_outline")
            success_message("Identifikasi hash selesai!")
        else:
            warning_message("Tidak dapat mengidentifikasi tipe hash!")
        
        input("\nTekan Enter untuk kembali ke menu...")

class HashCracker:
    def __init__(self):
        self.name = "Hash Cracker"
        self.description = "Memecahkan hash dengan wordlist"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        hash_value = validate_input("[?] Masukkan hash: ", str)
        wordlist_path = validate_input("[?] Masukkan path ke wordlist: ", str)
        
        if not os.path.exists(wordlist_path):
            error_message(f"File tidak ditemukan: {wordlist_path}")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        try:
            # Identifikasi tipe hash
            hash_type = None
            if len(hash_value) == 32:
                hash_type = 'md5'
            elif len(hash_value) == 40:
                hash_type = 'sha1'
            elif len(hash_value) == 64:
                hash_type = 'sha256'
            else:
                error_message("Tipe hash tidak didukung!")
                input("\nTekan Enter untuk kembali ke menu...")
                return
            
            print(f"\nMencoba memecahkan hash {hash_type}...")
            print(f"Menggunakan wordlist: {wordlist_path}")
            
            found = False
            attempts = 0
            start_time = time.time()
            
            with open(wordlist_path, 'r', errors='ignore') as f:
                lines = f.readlines()
                total_lines = len(lines)
                
                for line in lines:
                    attempts += 1
                    password = line.strip()
                    if not password:
                        continue
                    
                    # Hitung hash
                    if hash_type == 'md5':
                        computed_hash = hashlib.md5(password.encode()).hexdigest()
                    elif hash_type == 'sha1':
                        computed_hash = hashlib.sha1(password.encode()).hexdigest()
                    elif hash_type == 'sha256':
                        computed_hash = hashlib.sha256(password.encode()).hexdigest()
                    
                    # Tampilkan progress
                    if attempts % 100 == 0 or attempts == total_lines:
                        elapsed = time.time() - start_time
                        speed = attempts / elapsed if elapsed > 0 else 0
                        display_progress(attempts, total_lines, 
                                      prefix='Progress:', 
                                      suffix=f'Complete | Speed: {speed:.2f} h/s', 
                                      length=50)
                    
                    # Bandingkan hash
                    if computed_hash == hash_value:
                        print(f"\n\033[92m[✓] Password ditemukan: {password}\033[0m")
                        found = True
                        break
            
            if not found:
                print(f"\n\033[91m[✗] Password tidak ditemukan dalam {attempts} percobaan\033[0m")
                
        except Exception as e:
            error_message(f"Gagal memecahkan hash: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

class DataEncoderDecoder:
    def __init__(self):
        self.name = "Data Encoder/Decoder"
        self.description = "Utilitas konversi data (Base64, URL, Hex)"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        # Siapkan data untuk tabel operasi
        operations = [
            [1, "Base64 Encode", "Encode data ke Base64"],
            [2, "Base64 Decode", "Decode data dari Base64"],
            [3, "URL Encode", "Encode data ke format URL"],
            [4, "URL Decode", "Decode data dari format URL"],
            [5, "Hex Encode", "Encode data ke format Hex"],
            [6, "Hex Decode", "Decode data dari format Hex"]
        ]
        
        # Tampilkan operasi dalam tabel
        headers = ["ID", "Operasi", "Deskripsi"]
        display_result_table(operations, headers, title="Pilih Operasi", tablefmt="rounded_outline")
        
        choice = validate_input("\n[?] Pilih operasi (1-6): ", int, 1, lambda x: 1 <= x <= 6)
        data = validate_input("[?] Masukkan  ", str)
        
        try:
            if choice == 1:  # Base64 Encode
                result = base64.b64encode(data.encode()).decode()
                print(f"\nHasil Base64 Encode:")
            elif choice == 2:  # Base64 Decode
                result = base64.b64decode(data).decode()
                print(f"\nHasil Base64 Decode:")
            elif choice == 3:  # URL Encode
                result = urllib.parse.quote(data)
                print(f"\nHasil URL Encode:")
            elif choice == 4:  # URL Decode
                result = urllib.parse.unquote(data)
                print(f"\nHasil URL Decode:")
            elif choice == 5:  # Hex Encode
                result = data.encode().hex()
                print(f"\nHasil Hex Encode:")
            elif choice == 6:  # Hex Decode
                result = bytes.fromhex(data).decode()
                print(f"\nHasil Hex Decode:")
            
            # Tampilkan hasil dalam tabel
            headers = ["Hasil"]
            display_result_table([[result]], headers, title=None, tablefmt="rounded_outline")
            success_message("Operasi berhasil!")
            
        except Exception as e:
            error_message(f"Gagal melakukan operasi: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

# KATEGORI VI: FORENSICS, MALWARE ANALYSIS, & BLUE TEAM
class FileSignatureChecker:
    def __init__(self):
        self.name = "File Signature Checker"
        self.description = "Memverifikasi tipe file berdasarkan magic number-nya"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        file_path = validate_input("[?] Masukkan path ke file: ", str)
        if not os.path.exists(file_path):
            error_message(f"File tidak ditemukan: {file_path}")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        try:
            # Baca beberapa byte pertama file untuk magic number
            with open(file_path, 'rb') as f:
                magic_number = f.read(16)  # Baca 16 byte pertama
            
            # Daftar magic number untuk berbagai jenis file
            file_signatures = {
                b'\x25\x50\x44\x46': 'PDF',
                b'\x50\x4B\x03\x04': 'ZIP',
                b'\x50\x4B\x05\x06': 'ZIP (empty)',
                b'\x50\x4B\x07\x08': 'ZIP (spanned)',
                b'\x1F\x8B\x08': 'GZIP',
                b'\x42\x5A\x68': 'BZIP2',
                b'\x7F\x45\x4C\x46': 'ELF (Linux executable)',
                b'\x4D\x5A': 'EXE (Windows executable)',
                b'\x25\x21\x50\x53\x2D\x41\x64\x6F\x62\x65\x2D': 'PostScript',
                b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'PNG',
                b'\xFF\xD8\xFF': 'JPEG',
                b'\x47\x49\x46\x38\x37\x61': 'GIF87a',
                b'\x47\x49\x46\x38\x39\x61': 'GIF89a',
                b'\x49\x49\x2A\x00': 'TIFF (little endian)',
                b'\x4D\x4D\x00\x2A': 'TIFF (big endian)',
                b'\x00\x00\x01\x00': 'ICO',
                b'\x00\x00\x02\x00': 'CUR',
                b'\x46\x4C\x49\x46': 'FLIF',
                b'\x57\x45\x42\x50': 'WEBP',
                b'\x3C\x73\x76\x67': 'SVG',
                b'\x3C\x3F\x78\x6D\x6C': 'XML',
                b'\x7B\x5C\x72\x74\x66\x31': 'Rich Text Format (RTF)',
                b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1': 'Microsoft Office document',
                b'\x09\x04\x06\x00': 'Microsoft Office 2007+ document',
                b'\x50\x4B\x03\x04\x14\x00\x06\x00': 'Microsoft Office 2007+ document (ZIP-based)',
                b'\x7F\x45\x4C\x46': 'Unix executable',
                b'\xCA\xFE\xBA\xBE': 'Mach-O executable (fat)',
                b'\xFE\xED\xFA\xCE': 'Mach-O executable (32-bit)',
                b'\xFE\xED\xFA\xCF': 'Mach-O executable (64-bit)',
                b'\xCE\xFA\xED\xFE': 'Mach-O executable (32-bit, reverse)',
                b'\xCF\xFA\xED\xFE': 'Mach-O executable (64-bit, reverse)',
                b'\x23\x21': 'Script (shebang)',
                b'\xEF\xBB\xBF': 'UTF-8 with BOM',
                b'\xFF\xFE': 'UTF-16 little endian',
                b'\xFE\xFF': 'UTF-16 big endian',
                b'\xFF\xFE\x00\x00': 'UTF-32 little endian',
                b'\x00\x00\xFE\xFF': 'UTF-32 big endian'
            }
            
            detected_type = "Unknown"
            for signature, file_type in file_signatures.items():
                if magic_number.startswith(signature):
                    detected_type = file_type
                    break
            
            # Siapkan data untuk tabel
            results = [
                ["File", file_path],
                ["Magic Number (hex)", magic_number.hex().upper()],
                ["Tipe File", detected_type]
            ]
            
            # Dapatkan ekstensi file
            _, ext = os.path.splitext(file_path)
            if ext:
                results.append(["Ekstensi File", ext])
                # Periksa kecocokan ekstensi dengan tipe file
                if ext.lower() in ['.jpg', '.jpeg'] and detected_type != 'JPEG':
                    warning_message("Ekstensi file tidak cocok dengan tipe file sebenarnya!")
                elif ext.lower() == '.png' and detected_type != 'PNG':
                    warning_message("Ekstensi file tidak cocok dengan tipe file sebenarnya!")
                elif ext.lower() == '.pdf' and detected_type != 'PDF':
                    warning_message("Ekstensi file tidak cocok dengan tipe file sebenarnya!")
                elif ext.lower() == '.exe' and detected_type != 'EXE (Windows executable)':
                    warning_message("Ekstensi file tidak cocok dengan tipe file sebenarnya!")
            
            # Tampilkan hasil dalam tabel
            headers = ["Parameter", "Nilai"]
            display_result_table(results, headers, title=f"Hasil Analisis untuk {os.path.basename(file_path)}", tablefmt="rounded_outline")
            success_message("Analisis file selesai!")
            
        except Exception as e:
            error_message(f"Gagal menganalisis file: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

class NetworkConnectionMonitor:
    def __init__(self):
        self.name = "Network Connection Monitor"
        self.description = "Menampilkan koneksi jaringan aktif dan proses yang terkait"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        try:
            # Coba install psutil jika belum terinstall
            try:
                import psutil
            except ImportError:
                info_message("Menginstall psutil untuk monitoring koneksi jaringan...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
                import psutil
            
            print("\nMengumpulkan informasi koneksi jaringan...")
            # Dapatkan semua koneksi jaringan
            connections = psutil.net_connections(kind='inet')
            # Filter koneksi yang established dan listening
            active_connections = [conn for conn in connections if conn.status in ('ESTABLISHED', 'LISTEN')]
            
            if active_connections:
                print(f"Ditemukan {len(active_connections)} koneksi aktif:")
                
                # Siapkan data untuk tabel
                results = []
                for conn in active_connections[:20]:  # Batasi ke 20 koneksi pertama
                    try:
                        # Format local address
                        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                        # Format remote address
                        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                        # Dapatkan nama proses
                        pid = conn.pid
                        process_name = "N/A"
                        if pid:
                            try:
                                process = psutil.Process(pid)
                                process_name = process.name()
                            except:
                                pass
                        results.append([
                            str(pid),
                            process_name,
                            conn.status,
                            'TCP' if conn.type == socket.SOCK_STREAM else 'UDP',
                            laddr,
                            raddr
                        ])
                    except:
                        pass
                
                # Tampilkan hasil dalam tabel
                headers = ["PID", "Process", "Status", "Protocol", "Local Address", "Remote Address"]
                display_result_table(results, headers, title="Koneksi Jaringan Aktif", tablefmt="rounded_outline")
                
                if len(active_connections) > 20:
                    print(f"\n... dan {len(active_connections) - 20} koneksi lainnya")
                
                success_message("Monitoring koneksi jaringan selesai!")
            else:
                warning_message("Tidak ada koneksi aktif yang ditemukan!")
                
        except Exception as e:
            error_message(f"Gagal memonitor koneksi jaringan: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

# KATEGORI VII: UTILITIES & FUN PROJECTS
class SecureFileShredder:
    def __init__(self):
        self.name = "Secure File Shredder"
        self.description = "Menimpa file beberapa kali sebelum menghapusnya"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        file_path = validate_input("[?] Masukkan path ke file yang akan dihapus: ", str)
        if not os.path.exists(file_path):
            error_message(f"File tidak ditemukan: {file_path}")
            input("\nTekan Enter untuk kembali ke menu...")
            return
        
        try:
            # Konfirmasi penghapusan
            confirm = input(f"[?] Apakah Anda yakin ingin menghapus {file_path} secara permanen? (y/n): ").lower()
            if confirm != 'y':
                info_message("Penghapusan dibatalkan.")
                input("\nTekan Enter untuk kembali ke menu...")
                return
            
            # Dapatkan ukuran file
            file_size = os.path.getsize(file_path)
            print(f"\nMenghapus file {file_path} (Ukuran: {file_size} bytes)...")
            
            # Buka file untuk ditimpa
            with open(file_path, 'r+b') as f:
                # Pola penimpaan
                patterns = [
                    b'\x00',  # Nol
                    b'\xFF',  # Satu
                    b'\x55',  # Pola 01010101
                    b'\xAA',  # Pola 10101010
                    os.urandom(file_size)  # Data acak
                ]
                
                total_passes = len(patterns)
                for i, pattern in enumerate(patterns, 1):
                    # Kembali ke awal file
                    f.seek(0)
                    # Tentukan ukuran pola
                    pattern_size = len(pattern)
                    # Jika pola lebih kecil dari file, ulangi pola
                    if pattern_size < file_size:
                        repetitions = file_size // pattern_size
                        remainder = file_size % pattern_size
                        # Tulis pola berulang
                        for _ in range(repetitions):
                            f.write(pattern)
                        # Tulis sisa pola
                        if remainder > 0:
                            f.write(pattern[:remainder])
                    else:
                        # Jika pola lebih besar dari file, potong
                        f.write(pattern[:file_size])
                    # Flush perubahan ke disk
                    f.flush()
                    os.fsync(f.fileno())
                    
                    # Tampilkan progress
                    display_progress(i, total_passes, prefix='Menimpa:', suffix='Selesai', length=30)
            
            # Hapus file
            os.remove(file_path)
            success_message("File berhasil dihapus secara permanen!")
            
        except Exception as e:
            error_message(f"Gagal menghapus file: {str(e)}")
        
        input("\nTekan Enter untuk kembali ke menu...")

class MorseCodeTranslator:
    def __init__(self):
        self.name = "Morse Code Translator"
        self.description = "Menerjemahkan teks ke dan dari kode Morse"
    
    def run(self):
        clear_screen()
        print(f"=== {self.name} ===")
        print(f"{self.description}\n")
        
        # Siapkan data untuk tabel operasi
        operations = [
            [1, "Teks ke Morse", "Mengkonversi teks biasa ke kode Morse"],
            [2, "Morse ke Teks", "Mengkonversi kode Morse ke teks biasa"]
        ]
        
        # Tampilkan operasi dalam tabel
        headers = ["ID", "Operasi", "Deskripsi"]
        display_result_table(operations, headers, title="Pilih Operasi", tablefmt="rounded_outline")
        
        choice = validate_input("\n[?] Pilih operasi (1-2): ", int, 1, lambda x: 1 <= x <= 2)
        
        # Dictionary untuk konversi Morse
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
            "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
            '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
            '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
            ' ': '/'
        }
        # Reverse dictionary untuk konversi Morse ke teks
        reverse_morse_dict = {v: k for k, v in morse_dict.items()}
        
        if choice == 1:  # Teks ke Morse
            text = validate_input("[?] Masukkan teks: ", str).upper()
            morse_code = []
            for char in text:
                if char in morse_dict:
                    morse_code.append(morse_dict[char])
                else:
                    morse_code.append('?')
            result = ' '.join(morse_code)
            print(f"\nHasil Morse Code:")
        else:  # Morse ke Teks
            morse = validate_input("[?] Masukkan kode Morse (pisahkan dengan spasi): ", str)
            text = []
            for code in morse.split():
                if code in reverse_morse_dict:
                    text.append(reverse_morse_dict[code])
                else:
                    text.append('?')
            result = ''.join(text)
            print(f"\nHasil Teks:")
        
        # Tampilkan hasil dalam tabel
        headers = ["Hasil"]
        display_result_table([[result]], headers, title=None, tablefmt="rounded_outline")
        success_message("Konversi selesai!")
        
        input("\nTekan Enter untuk kembali ke menu...")