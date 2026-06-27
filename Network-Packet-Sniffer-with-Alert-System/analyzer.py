from alerts import alert

packet_count = {}

def detect(src_ip):

    if src_ip not in packet_count:
        packet_count[src_ip] = 0

    packet_count[src_ip] += 1

    if packet_count[src_ip] > 40:
        alert(f"Possible flooding attack from {src_ip}")
