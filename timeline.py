from pathlib import Path
from datetime import datetime


# Define the log files to read from the same directory as this script.
base_dir = Path(__file__).resolve().parent
auth_log = base_dir / "auth_events.log"
file_log = base_dir / "file_events.log"


# Read each log file and store its lines with their parsed timestamps.
def parse_log(path):
    events = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            # The first 19 characters contain the timestamp in YYYY-MM-DD HH:MM:SS format.
            timestamp = datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
            events.append((timestamp, line))
    return events


# Merge the events from both files into one list and sort by time.
all_events = parse_log(auth_log) + parse_log(file_log)
all_events.sort(key=lambda item: item[0])


# Print the timeline, highlighting important events.
for timestamp, line in all_events:
    message = line[19:].lstrip()
    marker = ""
    if "SUCCESS LOGIN" in line or ".locked" in line or "READ_ME" in line:
        marker = "*** KEY EVENT ***"
    print(f"{timestamp} {message} {marker}".strip())
