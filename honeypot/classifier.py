def analyze_session(commands):

    score = 0

    attack_types = set()

    for cmd in commands:

        cmd = cmd.lower()

        if "rm -rf" in cmd:

            score += 10

            attack_types.add("Destructive Attack")

        elif "hydra" in cmd:

            score += 6

            attack_types.add("Brute Force Attempt")

        elif "cat /etc/passwd" in cmd:

            score += 5

            attack_types.add("Privilege Enumeration")

        elif "wget" in cmd or "curl" in cmd:

            score += 4

            attack_types.add("Malicious Download Attempt")

        elif "nmap" in cmd:

            score += 3

            attack_types.add("Reconnaissance Attack")

        elif cmd in ["ls", "pwd", "whoami", "uname -a"]:

            score += 1

            attack_types.add("Reconnaissance")

        else:

            score += 1

            attack_types.add("General Suspicious Activity")


    # -----------------------------
    # Overall Severity
    # -----------------------------

    if score <= 4:

        severity = "LOW"

    elif score <= 10:

        severity = "MEDIUM"

    elif score <= 18:

        severity = "HIGH"

    else:

        severity = "CRITICAL"


    # -----------------------------
    # Overall Attack Type
    # Highest priority wins
    # -----------------------------

    priority = [

        "Destructive Attack",

        "Brute Force Attempt",

        "Privilege Enumeration",

        "Malicious Download Attempt",

        "Reconnaissance Attack",

        "Reconnaissance",

        "General Suspicious Activity"

    ]

    overall_attack = "General Suspicious Activity"

    for attack in priority:

        if attack in attack_types:

            overall_attack = attack

            break

    return {

        "severity": severity,

        "attack_type": overall_attack,

        "score": score

    }