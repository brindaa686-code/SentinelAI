import os

# Default to the pfirewall.log shipped in the project root, so the agent
# works out of the box without a hardcoded personal path.
DEFAULT_LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pfirewall.log"
)


def read_firewall_log(path=None):
    """
    Read every real log line (skipping comments/blank lines) so the
    detection engine can inspect each line's characteristics — not just
    ALLOW/DROP lines, since attacks like brute force or phishing show up
    in other line formats too.
    """
    path = path or DEFAULT_LOG_PATH
    entries = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            entries.append(line)
    return entries