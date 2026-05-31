import hashlib
import json
import os
from datetime import datetime

# File penyimpanan data user (JSON)
DATA_FILE = "data_users.json"

def hash_md5(password: str) -> str:
    """Menghasilkan hash MD5 dari password."""
    return hashlib.md5(password.encode()).hexdigest()

def hash_sha256(password: str) -> str:
    """Menghasilkan hash SHA-256 dari password."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users() -> dict:
    """Memuat data user dari file JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users: dict) -> None:
    """Menyimpan data user ke file JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def registrasi():
    print("\n" + "="*55)
    print("          📝  REGISTRASI AKUN BARU")
    print("="*55)

    users = load_users()

    username = input("Masukkan username : ").strip()
    if not username:
        print("❌  Username tidak boleh kosong.")
        return

    if username in users:
        print(f"❌  Username '{username}' sudah terdaftar.")
        return

    password = input("Masukkan password  : ").strip()
    if not password:
        print("❌  Password tidak boleh kosong.")
        return

    print("\nPilih algoritma hashing:")
    print("  [1] MD5")
    print("  [2] SHA-256")
    pilihan = input("Pilihan (1/2)      : ").strip()

    if pilihan == "1":
        algoritma = "MD5"
        hash_password = hash_md5(password)
    elif pilihan == "2":
        algoritma = "SHA-256"
        hash_password = hash_sha256(password)
    else:
        print("❌  Pilihan tidak valid.")
        return

    users[username] = {
        "password_hash": hash_password,
        "algoritma": algoritma,
        "terdaftar_pada": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_users(users)

    print("\n" + "-"*55)
    print("✅  Registrasi berhasil!")
    print(f"   Username        : {username}")
    print(f"   Password asli   : {password}")
    print(f"   Algoritma       : {algoritma}")
    print(f"   Hash password   : {hash_password}")
    print("-"*55)

def login():
    print("\n" + "="*55)
    print("          🔐  LOGIN PENGGUNA")
    print("="*55)

    users = load_users()

    username = input("Username : ").strip()
    password = input("Password : ").strip()

    if username not in users:
        print(f"\n❌  Username '{username}' tidak ditemukan.")
        return

    data = users[username]
    algoritma = data["algoritma"]
    stored_hash = data["password_hash"]

    if algoritma == "MD5":
        input_hash = hash_md5(password)
    else:
        input_hash = hash_sha256(password)

    print("\n" + "-"*55)
    print("🔍  PROSES VERIFIKASI LOGIN")
    print(f"   Algoritma          : {algoritma}")
    print(f"   Password diinput   : {password}")
    print(f"   Hash dari input    : {input_hash}")
    print(f"   Hash tersimpan     : {stored_hash}")
    print(f"   Hash cocok?        : {'✅ YA' if input_hash == stored_hash else '❌ TIDAK'}")
    print("-"*55)

    if input_hash == stored_hash:
        print(f"✅  Login berhasil! Selamat datang, {username}!")
    else:
        print("❌  Login gagal! Password salah.")

def lihat_data_user():
    print("\n" + "="*55)
    print("          📂  DATA USER TERSIMPAN")
    print("="*55)

    users = load_users()
    if not users:
        print("   (Belum ada user terdaftar)")
        return

    for i, (username, data) in enumerate(users.items(), 1):
        print(f"\n  User #{i}")
        print(f"   Username        : {username}")
        print(f"   Hash password   : {data['password_hash']}")
        print(f"   Algoritma       : {data['algoritma']}")
        print(f"   Terdaftar pada  : {data['terdaftar_pada']}")
        print(f"   (Password asli TIDAK disimpan ✅)")

def menu_utama():
    while True:
        print("\n" + "="*55)
        print("   🔒  SISTEM LOGIN - MD5 & SHA-256  🔒")
        print("="*55)
        print("  [1] Registrasi Akun")
        print("  [2] Login Pengguna")
        print("  [3] Lihat Data User Tersimpan")
        print("  [4] Keluar")
        print("="*55)

        pilihan = input("Pilih menu (1-4) : ").strip()

        if pilihan == "1":
            registrasi()
        elif pilihan == "2":
            login()
        elif pilihan == "3":
            lihat_data_user()
        elif pilihan == "4":
            print("\n👋  Terima kasih! Program selesai.\n")
            break
        else:
            print("❌  Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    menu_utama()
