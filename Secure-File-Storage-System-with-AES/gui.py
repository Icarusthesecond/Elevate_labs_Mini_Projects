import tkinter as tk
from tkinter import filedialog
import json
import os
from crypto_utils import encrypt_file, decrypt_file, calculate_hash

metadata_file = "metadata.json"

def encrypt_selected():

    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    encrypted_data = encrypt_file(file_path)

    hash_value = calculate_hash(encrypted_data)

    file_name = os.path.basename(file_path)

    enc_path = "encrypted_files/"+file_name+".enc"

    with open(enc_path,"wb") as f:
        f.write(encrypted_data)

    metadata = {
        "file": file_name,
        "hash": hash_value
    }

    with open(metadata_file,"a") as m:
        m.write(json.dumps(metadata)+"\n")

    status.config(text="File encrypted and stored securely")

def decrypt_selected():

    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    with open(file_path,"rb") as f:
        encrypted_data = f.read()

    decrypted = decrypt_file(encrypted_data)

    save_path = filedialog.asksaveasfilename()

    with open(save_path,"wb") as f:
        f.write(decrypted)

    status.config(text="File decrypted successfully")

root = tk.Tk()
root.title("Secure AES File Storage")
root.geometry("500x350")
root.configure(bg="#1e1e1e")

title = tk.Label(root,text="Secure File Storage System",
fg="cyan",bg="#1e1e1e",font=("Arial",16))
title.pack(pady=20)

encrypt_btn = tk.Button(
root,text="Encrypt File",
command=encrypt_selected,
bg="green",
fg="white",
width=20)

encrypt_btn.pack(pady=10)

decrypt_btn = tk.Button(
root,text="Decrypt File",
command=decrypt_selected,
bg="blue",
fg="white",
width=20)

decrypt_btn.pack(pady=10)

status = tk.Label(root,text="",fg="white",bg="#1e1e1e")
status.pack(pady=20)

root.mainloop()
