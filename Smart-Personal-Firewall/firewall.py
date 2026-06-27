from scapy.all import sniff
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import logging
from collections import defaultdict
import time

# ----------------------------
# CONFIG & STORAGE
# ----------------------------

rules = {
    "blocked_ips": [],
    "blocked_ports": []
}

packet_counter = 0
blocked_counter = 0
suspicious_counter = 0
firewall_active = False

ip_activity = defaultdict(list)

logging.basicConfig(filename="logs.txt", level=logging.INFO)

# ----------------------------
# RULE HANDLING
# ----------------------------

def save_rules():
    with open("rules.json", "w") as f:
        json.dump(rules, f)

def load_rules():
    global rules
    try:
        with open("rules.json", "r") as f:
            rules = json.load(f)
    except:
        pass

# ----------------------------
# PACKET PROCESSING
# ----------------------------

def packet_callback(packet):
    global packet_counter, blocked_counter, suspicious_counter

    if not firewall_active:
        return

    if packet.haslayer("IP"):
        packet_counter += 1
        update_counters()

        src_ip = packet["IP"].src
        current_time = time.time()

        # Track activity
        ip_activity[src_ip].append(current_time)
        ip_activity[src_ip] = [
            t for t in ip_activity[src_ip]
            if current_time - t < 5
        ]

        status = "NORMAL"
        color = "green"

        # Suspicious detection
        if len(ip_activity[src_ip]) > 10:
            suspicious_counter += 1
            status = "SUSPICIOUS"
            color = "orange"
            logging.info(f"Suspicious activity from {src_ip}")

        # Block IP
        if src_ip in rules["blocked_ips"]:
            blocked_counter += 1
            status = "BLOCKED"
            color = "red"
            logging.info(f"Blocked IP: {src_ip}")

        # Block Port
        if packet.haslayer("TCP"):
            port = packet["TCP"].dport
            if port in rules["blocked_ports"]:
                blocked_counter += 1
                status = "BLOCKED"
                color = "red"
                logging.info(f"Blocked Port: {port}")

        tree.insert("", "end", values=(src_ip, status, packet.summary()), tags=(color,))
        update_counters()

# ----------------------------
# FIREWALL CONTROL
# ----------------------------

def start_firewall():
    global firewall_active
    firewall_active = True
    status_label.config(text="Status: ACTIVE", fg="lime")

    threading.Thread(
        target=lambda: sniff(prn=packet_callback, store=False),
        daemon=True
    ).start()

def stop_firewall():
    global firewall_active
    firewall_active = False
    status_label.config(text="Status: STOPPED", fg="red")

# ----------------------------
# RULE MANAGEMENT
# ----------------------------

def block_ip():
    ip = ip_entry.get()
    if ip:
        rules["blocked_ips"].append(ip)
        save_rules()
        messagebox.showinfo("Success", f"Blocked IP {ip}")

def block_port():
    try:
        port = int(port_entry.get())
        rules["blocked_ports"].append(port)
        save_rules()
        messagebox.showinfo("Success", f"Blocked Port {port}")
    except:
        messagebox.showerror("Error", "Invalid Port")

# ----------------------------
# UTILITIES
# ----------------------------

def update_counters():
    total_label.config(text=f"Total Packets: {packet_counter}")
    blocked_label.config(text=f"Blocked: {blocked_counter}")
    suspicious_label.config(text=f"Suspicious: {suspicious_counter}")

def export_logs():
    messagebox.showinfo("Logs", "Logs saved in logs.txt")

def clear_table():
    for row in tree.get_children():
        tree.delete(row)

# ----------------------------
# GUI DESIGN (DARK THEME)
# ----------------------------

root = tk.Tk()
root.title("🔥 Smart Personal Firewall Dashboard")
root.geometry("1000x600")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background="#2e2e2e",
    foreground="white",
    fieldbackground="#2e2e2e"
)

style.map("Treeview",
    background=[("selected", "#444")]
)

# Top Panel
top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(pady=10)

status_label = tk.Label(top_frame, text="Status: STOPPED",
                        fg="red", bg="#1e1e1e", font=("Arial", 14))
status_label.pack()

# Buttons
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=5)

tk.Button(button_frame, text="Start Firewall",
          bg="green", fg="white",
          command=start_firewall).grid(row=0, column=0, padx=5)

tk.Button(button_frame, text="Stop Firewall",
          bg="red", fg="white",
          command=stop_firewall).grid(row=0, column=1, padx=5)

tk.Button(button_frame, text="Export Logs",
          command=export_logs).grid(row=0, column=2, padx=5)

tk.Button(button_frame, text="Clear",
          command=clear_table).grid(row=0, column=3, padx=5)

# Rule Section
rule_frame = tk.Frame(root, bg="#1e1e1e")
rule_frame.pack(pady=10)

ip_entry = tk.Entry(rule_frame)
ip_entry.grid(row=0, column=0, padx=5)
tk.Button(rule_frame, text="Block IP", command=block_ip).grid(row=0, column=1)

port_entry = tk.Entry(rule_frame)
port_entry.grid(row=1, column=0, padx=5)
tk.Button(rule_frame, text="Block Port", command=block_port).grid(row=1, column=1)

# Counters
counter_frame = tk.Frame(root, bg="#1e1e1e")
counter_frame.pack(pady=10)

total_label = tk.Label(counter_frame, text="Total Packets: 0",
                       fg="white", bg="#1e1e1e")
blocked_label = tk.Label(counter_frame, text="Blocked: 0",
                         fg="red", bg="#1e1e1e")
suspicious_label = tk.Label(counter_frame, text="Suspicious: 0",
                            fg="orange", bg="#1e1e1e")

total_label.pack()
blocked_label.pack()
suspicious_label.pack()

# Table
columns = ("Source IP", "Status", "Details")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Source IP", text="Source IP")
tree.heading("Status", text="Status")
tree.heading("Details", text="Packet Details")
tree.pack(fill="both", expand=True)

tree.tag_configure("green", foreground="lime")
tree.tag_configure("red", foreground="red")
tree.tag_configure("orange", foreground="orange")

load_rules()
root.mainloop()
