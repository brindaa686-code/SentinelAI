def detect_anomaly(log_entry: str) -> bool:
    """
    Detect anomalies in behavior or unusual patterns.
    Returns True if suspicious, False otherwise.
    """
    if len(log_entry) > 200 or "!!!" in log_entry:
        return True
    return False