# ======================================================
# CLASSIFY A SINGLE COMMAND
# Used by the Live Honeypot Terminal
# ======================================================

def classify_command(cmd):

    cmd = cmd.lower().strip()

    # -----------------------------
    # CRITICAL
    # -----------------------------

    if "rm -rf" in cmd:

        return "Destructive Attack"

    # -----------------------------
    # HIGH
    # -----------------------------

    elif "hydra" in cmd:

        return "Brute Force Attempt"

    elif "wget" in cmd or "curl" in cmd:

        return "Malicious Download Attempt"

    # -----------------------------
    # MEDIUM
    # -----------------------------

    elif "cat /etc/passwd" in cmd:

        return "Privilege Enumeration"

    elif "nmap" in cmd:

        return "Reconnaissance Attack"

    # -----------------------------
    # LOW
    # -----------------------------

    elif cmd in [

        "ls",

        "pwd",

        "whoami",

        "uname -a"

    ]:

        return "Reconnaissance"

    return "General Suspicious Activity"


# ======================================================
# ANALYZE COMPLETE SESSION
# Used for the Threat Severity card
# ======================================================

def analyze_session(commands):

    severity = "LOW"

    for cmd in commands:

        cmd = cmd.lower()

        # Highest priority
        if "rm -rf" in cmd:

            severity = "CRITICAL"

            break

        # HIGH
        elif (

            "hydra" in cmd or

            "wget" in cmd or

            "curl" in cmd

        ):

            if severity != "CRITICAL":

                severity = "HIGH"

        # MEDIUM
        elif (

            "nmap" in cmd or

            "cat /etc/passwd" in cmd

        ):

            if severity == "LOW":

                severity = "MEDIUM"

    return {

        "severity": severity

    }
