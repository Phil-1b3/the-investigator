from collections import Counter
import re
from pathlib import Path

# Open the log file in the same folder as this script
log_file = Path(__file__).with_name("server_access.log")

# Read all lines from the log file
with log_file.open("r", encoding="utf-8") as file:
    lines = file.readlines()

# Find lines containing failed login attempts and extract IP addresses
ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
ips = []
for line in lines:
    if "FAILED LOGIN" in line:
        match = ip_pattern.search(line)
        if match:
            ips.append(match.group(0))

# Count how many times each IP appears
counts = Counter(ips)

# Print a clean summary sorted by most attempts first
print("=== Failed Login Summary ===")
for ip, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
    print(f"{ip}: {count}")
