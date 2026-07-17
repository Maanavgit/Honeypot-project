import os
from datetime import datetime

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)


def create_session_log(session_id=None):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = os.path.join(

        LOG_DIR,

        f"attack_session_{timestamp}.log"

    )

    with open(filename, "w") as f:

        f.write(f"Session Started : {datetime.now()}\n\n")

    return filename


def log_command(filename, ip, command):

    with open(filename, "a") as f:

        f.write(f"[{datetime.now()}] {ip} -> {command}\n")
