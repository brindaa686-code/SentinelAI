SEVERITY_WEIGHTS = {
    "Brute Force": 3,
    "Unauthorized Access": 3,
    "Phishing": 2,
    "IP Abuse": 2,
    "Spam": 1,
    "Anomaly": 1,
}


def score_finding(finding: dict) -> dict:
    """
    Turn one finding (a log line plus the attack characteristics it
    matched) into a numeric risk score and severity label.
    """
    score = sum(SEVERITY_WEIGHTS.get(attack, 1) for attack in finding["attacks"])
    if score >= 5:
        severity = "high"
    elif score >= 2:
        severity = "medium"
    else:
        severity = "low"
    return {**finding, "risk_score": score, "severity": severity}


def score_findings(findings: list) -> list:
    return [score_finding(f) for f in findings]