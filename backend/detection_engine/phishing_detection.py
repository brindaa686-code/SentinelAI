def detect_phishing(log_entry: str) -> bool:
    """
    Detect phishing attempts in a log entry.
    Returns True if suspicious, False otherwise.
    """
    phishing_keywords = ["http://", "https://", "login", "verify", "account"]
    return any(keyword in log_entry.lower() for keyword in phishing_keywords)