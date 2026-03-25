import re
import pandas as pd
import matplotlib.pyplot as plt

log_file = "sample.log"

ip_pattern = r'(\d+\.\d+\.\d+\.\d+)'
failed_login_pattern = r'Failed password'

ips = []
failed_attempts = {}

# -------- READ LOG --------
with open(log_file, "r") as file:
    for line in file:
        ip_match = re.search(ip_pattern, line)

        if ip_match:
            ip = ip_match.group()
            ips.append(ip)

            if re.search(failed_login_pattern, line):
                failed_attempts[ip] = failed_attempts.get(ip, 0) + 1

# -------- DATAFRAME --------
df = pd.DataFrame(ips, columns=["IP"])
ip_counts = df["IP"].value_counts()

# -------- BRUTE FORCE DETECTION --------
print("\n🚨 Brute Force Detection:")
for ip, count in failed_attempts.items():
    if count > 3:
        print(f"{ip} → {count} failed attempts")

# -------- DOS DETECTION --------
print("\n⚡ DoS Detection:")
for ip, count in ip_counts.items():
    if count > 5:
        print(f"{ip} → High traffic ({count} requests)")

# -------- BLACKLIST CHECK --------
blacklist = ["192.168.1.10"]

print("\n🚫 Blacklisted IPs:")
for ip in ips:
    if ip in blacklist:
        print(f"{ip} is BLACKLISTED")

# -------- VISUALIZATION --------
ip_counts.head(5).plot(kind='bar')
plt.title("Top 5 IPs Accessing System")
plt.xlabel("IP Address")
plt.ylabel("Requests")
plt.show()

# -------- EXPORT REPORT --------
with open("report.txt", "w") as report:
    report.write("=== Intrusion Detection Report ===\n\n")

    report.write("Brute Force:\n")
    for ip, count in failed_attempts.items():
        if count > 3:
            report.write(f"{ip} → {count} failed attempts\n")

    report.write("\nDoS Detection:\n")
    for ip, count in ip_counts.items():
        if count > 5:
            report.write(f"{ip} → {count} requests\n")

    report.write("\nBlacklisted IPs:\n")
    for ip in ips:
        if ip in blacklist:
            report.write(f"{ip} detected\n")

# -------- EXPORT CSV --------
ip_counts.to_csv("ip_report.csv")

print("\n✅ Report saved (report.txt & ip_report.csv)")
