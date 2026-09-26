def detect_unauthorized(log_entry: str) -> bool:
    """
    Detect unauthorized access attempts in a log entry.
    Returns True if suspicious, False otherwise.
    """
    if "UNAUTHORIZED" in log_entry.upper() or "ACCESS DENIED" in log_entry.upper():
        return True
    return False