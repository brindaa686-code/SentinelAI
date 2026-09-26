def detect_ip_abuse(log_entry: str) -> bool:
    """
    Detect IP abuse (e.g., repeated requests from same IP).
    Returns True if suspicious, False otherwise.
    """
    suspicious_ips = ["192.168.1.10", "10.0.0.5"]  # Example IPs
    return any(ip in log_entry for ip in suspicious_ips)