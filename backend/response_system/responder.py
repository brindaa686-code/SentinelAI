import re

from response_system.block_ip import block_ip
from response_system.quarantine import quarantine
from response_system.send_alerts import send_alert
from response_system.log_event import log_event

IP_PATTERN = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")


def extract_ip(text: str) -> str:
    match = IP_PATTERN.search(text)
    return match.group(0) if match else "unknown"


def respond(scored_finding: dict) -> str:
    """
    Decide what action to take based on severity. Every finding gets
    logged; medium/high severity also gets an alert, and high severity
    additionally blocks the source IP.
    """
    ip = extract_ip(scored_finding["log_entry"])
    summary = (
        f"{', '.join(scored_finding['attacks'])} from {ip} "
        f"(risk={scored_finding['risk_score']}, severity={scored_finding['severity']})"
    )

    log_event(summary)

    if scored_finding["severity"] == "high":
        block_ip(ip)
        send_alert(f"HIGH severity threat: {summary}")
    elif scored_finding["severity"] == "medium":
        send_alert(f"MEDIUM severity threat: {summary}")

    return summary