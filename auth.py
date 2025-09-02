#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#===========================================
#  Tools Created By Xbibz Official!                     
#     Do Not Recode!                         
# Youtube : https://youtube.com/@XbibzOfficial
# TikTok  : https://tiktok.com/@xbibzofficiall
#===========================================



import os
import requests
import json
import base64
import getpass
import hashlib
from utils import error_message, success_message, info_message, display_result_table

class AuthManager:
    
    def __init__(self, github_pat, repo_owner, repo_name, file_path="users.json"):
        if not github_pat or not repo_owner or not repo_name:
            raise ValueError("GitHub PAT, repository owner, and repository name must be provided.")
            
        self.github_pat = github_pat
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.file_path = file_path
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        self.raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{file_path}"
        self.headers = {
            "Authorization": f"token {self.github_pat}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _hash_password(self, password):
        
        salt = os.urandom(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt.hex() + ':' + pwd_hash.hex()

    def _verify_password(self, stored_password, provided_password):
        
        try:
            salt_hex, hash_hex = stored_password.split(':')
            salt = bytes.fromhex(salt_hex)
            pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
            return pwd_hash.hex() == hash_hex
        except (ValueError, TypeError):
            return False

    def _get_users_from_github(self):
        
        try:
            response = requests.get(self.raw_url)
            if response.status_code == 200:
                return json.loads(response.text)
            elif response.status_code == 404:
                info_message("File pengguna tidak ditemukan di GitHub. Membuat struktur baru.")
                return {"users": []}
            else:
                error_message(f"Gagal mengambil data pengguna dari GitHub (Status: {response.status_code}).")
                return None
        except requests.exceptions.RequestException as e:
            error_message(f"Kesalahan jaringan saat mengambil data pengguna: {e}")
            return None
        except json.JSONDecodeError:
            error_message("Gagal mem-parsing data pengguna dari GitHub. File mungkin korup.")
            return None

    def _write_users_to_github(self, user_data, message):
        
        try:
            # Get the current file SHA
            get_response = requests.get(self.api_url, headers=self.headers)
            sha = None
            if get_response.status_code == 200:
                sha = get_response.json().get('sha')
            elif get_response.status_code != 404:
                error_message(f"Gagal mendapatkan SHA file dari GitHub (Status: {get_response.status_code}).")
                return False

            content_bytes = json.dumps(user_data, indent=4).encode('utf-8')
            content_base64 = base64.b64encode(content_bytes).decode('utf-8')

            payload = {
                "message": message,
                "content": content_base64
            }
            if sha:
                payload["sha"] = sha

            put_response = requests.put(self.api_url, headers=self.headers, json=payload)

            if put_response.status_code in [200, 201]:
                success_message("Data pengguna berhasil diperbarui di GitHub.")
                return True
            else:
                error_message(f"Gagal menulis data pengguna ke GitHub (Status: {put_response.status_code}).")
                print(put_response.json())
                return False
        except requests.exceptions.RequestException as e:
            error_message(f"Kesalahan jaringan saat menulis data pengguna: {e}")
            return False

    def login(self):
        
        for attempt in range(3):
            info_message("Silakan login untuk melanjutkan.")
            username = input("[?] Username: ")
            password = getpass.getpass("[?] Password: ")

            user_data = self._get_users_from_github()
            if user_data is None:
                return None, None

            for user in user_data.get("users", []):
                if user["username"] == username and self._verify_password(user["password"], password):
                    success_message(f"Login berhasil! Selamat datang, {username} ({user['role']}).")
                    return username, user["role"]
            
            error_message(f"Username atau password salah. Sisa percobaan: {2 - attempt}")
        
        error_message("Gagal login setelah 3 kali percobaan.")
        return None, None

    def add_user(self):
        
        info_message("Menambahkan Pengguna Baru")
        username = input("[?] Masukkan username baru: ")
        password = getpass.getpass("[?] Masukkan password baru: ")
        role = input("[?] Masukkan peran (owner/user) [default: user]: ").lower() or "user"
        if role not in ["owner", "user"]:
            error_message("Peran tidak valid. Harus 'owner' atau 'user'.")
            return

        user_data = self._get_users_from_github()
        if user_data is None:
            return

        if any(u['username'] == username for u in user_data['users']):
            error_message(f"Username '{username}' sudah ada.")
            return

        hashed_password = self._hash_password(password)
        user_data['users'].append({"username": username, "password": hashed_password, "role": role})

        self._write_users_to_github(user_data, f"Add user {username}")

    def delete_user(self):
        
        info_message("Menghapus Pengguna")
        username = input("[?] Masukkan username yang akan dihapus: ")
        
        user_data = self._get_users_from_github()
        if user_data is None:
            return

        original_user_count = len(user_data['users'])
        user_data['users'] = [u for u in user_data['users'] if u['username'] != username]

        if len(user_data['users']) < original_user_count:
            self._write_users_to_github(user_data, f"Delete user {username}")
        else:
            error_message(f"Pengguna '{username}' tidak ditemukan.")

    def list_users(self):
        
        info_message("Daftar Pengguna")
        user_data = self._get_users_from_github()
        if user_data is None:
            return

        users = user_data.get("users", [])
        if not users:
            info_message("Tidak ada pengguna yang terdaftar.")
            return
            
        table_data = [[u['username'], u['role']] for u in users]
        headers = ["Username", "Role"]
        display_result_table(table_data, headers, title="Pengguna Terdaftar")