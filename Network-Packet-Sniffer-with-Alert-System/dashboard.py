import sqlite3
import matplotlib.pyplot as plt

conn=sqlite3.connect("logs/packets.db")
cur=conn.cursor()

cur.execute("SELECT protocol,COUNT(*) FROM packets GROUP BY protocol")

data=cur.fetchall()

labels=[x[0] for x in data]
values=[x[1] for x in data]

plt.bar(labels,values)

plt.title("Network Traffic Distribution")
plt.xlabel("Protocol")
plt.ylabel("Packets")

plt.show()
