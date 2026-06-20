import os
from datetime import datetime

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

def create_session_log(session_id):

    filename = os.path.join(LOG_DIR, f"{session_id}.log")

    with open(filename, "w") as f:
        f.write(f"Session ID: {session_id}\n")
        f.write(f"Started: {datetime.now()}\n\n")

    return filename


def log_command(filename, ip, command):

    with open(filename, "a") as f:
        f.write(f"[{datetime.now()}] {ip} -> {command}\n")