from cryptography.fernet import Fernet
import os


KEY_FILE = "key.key"
PW_FILE = "pw.dat"
USERNAME_FILE = "username.txt"

#--private key
def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        #read binary
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        #write binary 
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    return key


def save_zugangsdaten(daten: dict):
    key = load_or_generate_key()
    fernet = Fernet(key)

    encrypted_pw = fernet.encrypt(daten["passwort"].encode())

    with open(PW_FILE, "wb") as f:
        f.write(encrypted_pw)

    with open(USERNAME_FILE, "w") as f:
        f.write(daten["username"])


def load_zugangsdaten():
    key = load_or_generate_key()
    fernet = Fernet(key)

    with open("username.txt", "r") as f:
        username = f.read()

    with open("pw.dat", "rb") as f:
        encrypted_pw = f.read()

    passwort = fernet.decrypt(encrypted_pw).decode()

    return {
        "username": username,
        "passwort": passwort
    }