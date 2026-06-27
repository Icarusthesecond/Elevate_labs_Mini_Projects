import tkinter as tk
import sqlite3

root=tk.Tk()

root.title("Smart Network IDS")
root.geometry("500x300")
root.configure(bg="black")

title=tk.Label(root,
text="Smart Packet Sniffer Dashboard",
fg="cyan",
bg="black",
font=("Arial",16))

title.pack(pady=20)


def stats():

    conn=sqlite3.connect("logs/packets.db")
    cur=conn.cursor()

    cur.execute("SELECT COUNT(*) FROM packets")

    total=cur.fetchone()[0]

    result.config(text=f"Packets Captured: {total}")


btn=tk.Button(root,
text="Show Statistics",
command=stats,
bg="cyan")

btn.pack(pady=10)

result=tk.Label(root,
text="",
fg="white",
bg="black")

result.pack()

root.mainloop()
