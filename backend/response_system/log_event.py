def log_event(event):
    with open("security_log.txt", "a") as f:
        f.write(event + "\n")
    print(f"[LOGGED] {event}")