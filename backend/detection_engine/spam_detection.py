def detect_spam(log_entry: str) -> bool:
    """
    Detect spam-related activity in a log entry.
    Returns True if suspicious, False otherwise.
    """
    spam_keywords = ["WIN MONEY", "FREE OFFER", "CLICK HERE"]
    return any(keyword in log_entry.upper() for keyword in spam_keywords)