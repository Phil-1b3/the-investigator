from datetime import datetime
from pathlib import Path
import os

# Import the Ollama client for local model access.
try:
    from ollama import Client
except ImportError as exc:  # pragma: no cover - import dependency guard
    raise SystemExit("Install the ollama Python package first: pip install ollama") from exc


def read_text_file(path: Path) -> str:
    """Read a file as text, preserving content and handling encoding issues."""
    return path.read_text(encoding="utf-8", errors="replace")


def build_evidence_payload(evidence_dir: Path) -> str:
    """Read every log file in the evidence folder and combine them into one prompt payload."""
    parts = []
    for path in sorted(evidence_dir.iterdir()):
        if path.is_file():
            parts.append(f"===== {path.name} =====\n{read_text_file(path)}")
    return "\n\n".join(parts)


def get_report_text(client: Client, evidence_text: str, runbook_text: str) -> str:
    """Send the evidence and runbook to the local Ollama model and return the Markdown report."""
    system_prompt = (
        "You are a senior SOC analyst. Review the supplied incident evidence and runbook, "
        "then produce a concise Markdown incident report with sections for summary, timeline, "
        "root cause, a MITRE ATT&CK mapping with tactic, technique name, and technique ID, "
        "which runbook steps were completed versus missed, and recommended next actions."
    )
    user_prompt = (
        "Incident evidence logs:\n\n"
        f"{evidence_text}\n\n"
        "Incident-response runbook:\n\n"
        f"{runbook_text}"
    )

    response = client.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    # Handle both dict-style and object-style responses from the Ollama client.
    if hasattr(response, "message") and hasattr(response.message, "content"):
        return response.message.content
    if isinstance(response, dict):
        message = response.get("message", {})
        if isinstance(message, dict):
            return message.get("content", "")
    return str(response)


def main() -> None:
    """Run the triage workflow, create a timestamped report, and write the generated Markdown."""
    base_dir = Path(__file__).resolve().parent
    evidence_dir = base_dir / "evidence"
    runbook_path = base_dir / "ir_runbook.md"
    reports_dir = base_dir / "reports"

    # Create the reports folder if it does not already exist.
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Read the evidence files and the runbook from disk.
    evidence_text = build_evidence_payload(evidence_dir)
    runbook_text = read_text_file(runbook_path)

    # Connect to the local Ollama service on the default host.
    ollama_host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
    client = Client(host=ollama_host)

    # Generate the incident report using the local model.
    report_text = get_report_text(client, evidence_text, runbook_text)

    # Write the result to a timestamped filename so repeated runs do not overwrite each other.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    report_path = reports_dir / f"report_{timestamp}.md"
    report_path.write_text(report_text, encoding="utf-8")

    print(f"Wrote report to {report_path}")


if __name__ == "__main__":
    main()
