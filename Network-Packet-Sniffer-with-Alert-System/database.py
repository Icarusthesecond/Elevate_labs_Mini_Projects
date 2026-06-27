import sqlite3

def init_db():

    conn = sqlite3.connect("logs/packets.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS packets(
        id INTEGER PRIMARY KEY,
        src_ip TEXT,
        dst_ip TEXT,
        protocol TEXT,
        length INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_packet(src,dst,proto,length,time):

    conn = sqlite3.connect("logs/packets.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO packets(src_ip,dst_ip,protocol,length,timestamp)
    VALUES(?,?,?,?,?)
    """,(src,dst,proto,length,time))

    conn.commit()
    conn.close()
