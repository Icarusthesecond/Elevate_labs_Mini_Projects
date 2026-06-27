import subprocess
import threading
import os

print("\n🚀 Starting Smart Network IDS...\n")

# start packet sniffer
def run_sniffer():
    os.system("sudo /home/kali/smart_sniffer/venv/bin/python sniffer.py")

# start GUI dashboard
def run_gui():
    os.system("python gui.py")

# start traffic graph
def run_dashboard():
    os.system("python dashboard.py")


t1 = threading.Thread(target=run_sniffer)
t2 = threading.Thread(target=run_gui)
t3 = threading.Thread(target=run_dashboard)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
