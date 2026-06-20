def classify_attack(commands):

    latest = commands[-1].lower()

    if "wget" in latest or "curl" in latest:
        return "Malicious Download Attempt"

    if "nmap" in latest:
        return "Reconnaissance Attack"

    if "hydra" in latest:
        return "Brute Force Attempt"

    if "cat /etc/passwd" in latest:
        return "Privilege Enumeration"

    if "rm -rf" in latest:
        return "Destructive Attack"

    return "General Suspicious Activity"