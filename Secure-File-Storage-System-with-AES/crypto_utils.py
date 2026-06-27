from cryptography.fernet import Fernet
import hashlib

# Generate encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as f:
        f.write(key)

def load_key():
    return open("key.key","rb").read()

# AES Encryption
def encrypt_file(file_path):

    key = load_key()
    f = Fernet(key)

    with open(file_path,"rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)

    return encrypted

# AES Decryption
def decrypt_file(encrypted_data):

    key = load_key()
    f = Fernet(key)

    return f.decrypt(encrypted_data)

# Hash for integrity
def calculate_hash(data):

    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()
