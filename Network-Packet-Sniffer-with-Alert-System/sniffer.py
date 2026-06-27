from scapy.all import sniff
from scapy.layers.inet import IP,TCP,UDP
import datetime

from database import insert_packet,init_db
from analyzer import detect

init_db()

def process_packet(packet):

    if packet.haslayer(IP):

        src = packet[IP].src
        dst = packet[IP].dst
        length = len(packet)

        proto = "OTHER"

        if packet.haslayer(TCP):
            proto="TCP"

        elif packet.haslayer(UDP):
            proto="UDP"

        time=str(datetime.datetime.now())

        insert_packet(src,dst,proto,length,time)

        detect(src)

        print(f"{src} -> {dst} | {proto} | {length}")


print("\nSmart Network IDS Running...\n")

sniff(prn=process_packet,store=False)
