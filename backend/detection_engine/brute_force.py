def detect_bruteforce(log_entry: str) -> bool:
    """
    Detect brute force login attempts in a log entry.
    Returns True if suspicious, False otherwise.
    """
    if "FAILED LOGIN" in log_entry.upper():
        return True
    return False