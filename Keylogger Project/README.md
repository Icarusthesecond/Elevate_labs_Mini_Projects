# Encrypted Keylogger PoC (Proof of Concept)

## ⚠️ Disclaimer
**This project is strictly for educational purposes, ethical hacking, and authorized security auditing.** The code provided here demonstrates how threat actors capture, encrypt, and exfiltrate data to help security professionals understand and build better Endpoint Detection and Response (EDR) defenses. Do not use this tool on any system or network without explicit, written permission from the owner. The author is not responsible for any misuse or damage caused by this software.

## 📖 Overview
This project is a Proof-of-Concept (PoC) Python keylogger that captures keystrokes, secures the logged data using symmetric AES encryption (Fernet), and simulates exfiltration to a remote server. 

To ensure safety during testing, the exfiltration is hardcoded to target `localhost`, and a strict "Kill Switch" is integrated to instantly terminate the process.

[Image of keylogger encryption and exfiltration architecture]

## ✨ Features
* **Keystroke Capture:** Monitors and records keyboard inputs seamlessly using `pynput`.
* **Symmetric Encryption:** Uses `cryptography.fernet` to encrypt the payload before it is written to disk or sent over the network, preventing plain-text credential dumping.
* **Network Exfiltration Simulation:** Base64-encodes the encrypted payload and transmits it via HTTP POST requests to a local listener.
* **Kill Switch:** Built-in emergency stop (pressing the `ESC` key) immediately halts the listener and terminates the script.
* **Decryption Utility:** Includes a dedicated decryption script to reverse the AES encryption on intercepted network traffic or local log files.

## 🛠️ Prerequisites