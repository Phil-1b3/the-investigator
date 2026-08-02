import os
from datetime import datetime
from pathlib import Path

import ollama

# Read the incident evidence logs from the evidence folder.
base_dir = Path(__file__).resolve().parent
evidence_dir = base_dir / "evidence"
runbook_path = base_dir / "ir_runbook.md"

# Combine all evidence files into one prompt payload.
prompt_parts = []
for path in sorted(evidence_dir.iterdir()):
    if path.is_file():
        prompt_parts.append(f"===== {path.name} =====\n{path.read_text(encoding='utf-8', errors='replace')}")

# Read the incident-response runbook.
runbook_text = runbook_path.read_text(encoding="utf-8", errors="replace")

# Build the prompt for the local model.
prompt_text = (
    "Incident evidence logs:\n\n"
    f"{'\n\n'.join(prompt_parts)}\n\n"
    "Incident-response runbook:\n\n"
    f"{runbook_text}"
)

# Send the prompt to the local Ollama model.
resp = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a senior SOC analyst. "
                "Map findings to MITRE ATT&CK with technique IDs and cite the runbook."
            ),
        },
        {"role": "user", "content": prompt_text},
    ],
)
report = resp.message.content

# Create the reports folder if it does not exist.
os.makedirs("reports", exist_ok=True)

# Write a timestamped report so each run produces a unique output file.
stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
with open(f"reports/report_{stamp}.md", "w", encoding="utf-8") as handle:
    handle.write(report)

print(f"Wrote report to reports/report_{stamp}.md")
