from collections import defaultdict
from pathlib import Path

# Open the traffic log in the same folder as this script
log_file = Path(__file__).with_name("network_traffic.log")

# Read all lines from the log file
with log_file.open("r", encoding="utf-8") as file:
    lines = file.readlines()

# Store each connection count and the timestamps seen for each pair
pair_counts = defaultdict(int)
pair_timestamps = defaultdict(list)

# Parse each line and track the source/destination pair
for line in lines:
    line = line.strip()
    if not line:
        continue

    parts = line.split()
    time = parts[0]
    source = parts[1]
    destination = parts[3]
    pair = f"{source} -> {destination}"

    pair_counts[pair] += 1
    pair_timestamps[pair].append(time)

# Find the pair with the most connections
most_common_pair = max(pair_counts.items(), key=lambda item: item[1])[0]
connection_count = pair_counts[most_common_pair]
timestamps = pair_timestamps[most_common_pair]

# Print the suspicious beaconing summary
print("=== Beaconing Suspect ===")
print(f"Pair: {most_common_pair}")
print(f"Connections: {connection_count}")
print("Timestamps:", ", ".join(timestamps))
