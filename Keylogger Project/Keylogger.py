from cryptography.fernet import Fernet
import datetime

# 1. Key Generation (Do this once and save it)
# key = Fernet.generate_key()
# with open("secret.key", "wb") as key_file:
#     key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_log(data):
    key = load_key()
    f = Fernet(key)
    
    # Add a timestamp for SOC-style log analysis
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {data}".encode()
    
    # Encrypt the byte string
    encrypted_data = f.encrypt(log_entry)
    
    # Append to your local log file
    with open("logs.dat", "ab") as f_log:
        f_log.write(encrypted_data + b"\n")

# Example usage:
# encrypt_log("User typed: 'password123'")
