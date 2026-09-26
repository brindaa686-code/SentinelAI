from datetime import datetime

from detection_engine.anomaly_detection import detect_anomaly
from detection_engine.brute_force import detect_bruteforce
from detection_engine.ip_abuse import detect_ip_abuse
from detection_engine.phishing_detection import detect_phishing
from detection_engine.spam_detection import detect_spam
from detection_engine.unauthorized_access import detect_unauthorized

# Each detector looks at one "character" (pattern/keyword) of a log line.
DETECTORS = [
    ("Brute Force", detect_bruteforce),
    ("Phishing", detect_phishing),
    ("IP Abuse", detect_ip_abuse),
    ("Unauthorized Access", detect_unauthorized),
    ("Spam", detect_spam),
    ("Anomaly", detect_anomaly),
]


def analyze_entry(log_entry: str) -> list:
    """
    Run every detector against a single log line. Returns the list of
    attack names whose characteristic pattern matched this line.
    """
    hits = []
    for attack_name, detector in DETECTORS:
        try:
            if detector(log_entry):
                hits.append(attack_name)
        except Exception:
            continue
    return hits


def analyze_log(entries: list) -> list:
    """
    Run the full detector set across many log lines. Returns a structured
    finding per line that matched at least one detector.
    """
    findings = []
    for entry in entries:
        attacks = analyze_entry(entry)
        if attacks:
            findings.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "log_entry": entry,
                "attacks": attacks,
            })
    return findings