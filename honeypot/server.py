import socket
import threading
from datetime import datetime

from honeypot.session import Session
from honeypot.classifier import analyze_session
from logger.logger import create_session_log, log_command


HOST = "0.0.0.0"
PORT = 2222


# ======================================================
# ONLY ONE ATTACKER ALLOWED
# ======================================================

active_session = False

session_lock = threading.Lock()


# ======================================================
# LIVE DASHBOARD DATA
# ======================================================

dashboard_data = {

    "ip": "",

    "severity": "",

    "attack_type": "",

    "score": 0,

    "commands": [],

    "command_log": [],

    "timeline": [],

    "login_attempts": [],

    "session_start": ""
}


# ======================================================
# FAKE TERMINAL
# ======================================================

def fake_shell_response(cmd):

    cmd = cmd.lower()

    if cmd == "ls":

        return "Documents  Downloads  secret.txt  passwords.txt\n$ "

    elif cmd == "pwd":

        return "/home/admin\n$ "

    elif cmd == "whoami":

        return "admin\n$ "

    elif cmd == "uname -a":

        return "Linux ubuntu 5.15.0-84-generic x86_64 GNU/Linux\n$ "

    elif "cat" in cmd:

        return "Permission denied\n$ "

    elif "sudo" in cmd:

        return "[sudo] password for admin:\nSorry, try again.\n$ "

    elif "wget" in cmd or "curl" in cmd:

        return "Connecting...\nDownload failed.\n$ "

    elif "nmap" in cmd:

        return "Starting Nmap scan...\nHost seems down.\n$ "

    elif "rm -rf" in cmd:

        return "rm: dangerous operation blocked\n$ "

    elif cmd == "exit":

        return "logout\n"

    else:

        return f"bash: {cmd}: command not found\n$ "


# ======================================================
# CLIENT HANDLER
# ======================================================

def handle_client(conn, addr):

    global active_session

    ip = addr[0]

    # ------------------------------------
    # ONLY ONE ATTACKER ALLOWED
    # ------------------------------------

    with session_lock:

        if active_session:

            print(f"[BLOCKED] Second connection from {ip}")

            conn.send(

                b"\nServer Busy.\n"
                b"Maximum one attacker session is allowed.\n"
                b"Please try again later.\n"

            )

            conn.close()

            return

        active_session = True


    print(f"\n[+] Connection received from {ip}")


    session = Session(ip)

    log_file = create_session_log(session.id)


    # ------------------------------------
    # RESET DASHBOARD
    # ------------------------------------

    dashboard_data["ip"] = ip

    dashboard_data["severity"] = ""

    dashboard_data["attack_type"] = ""

    dashboard_data["score"] = 0

    dashboard_data["commands"] = []

    dashboard_data["command_log"] = []

    dashboard_data["timeline"] = []

    dashboard_data["login_attempts"] = []

    dashboard_data["session_start"] = datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )

    try:

        conn.send(

            b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\n"

        )

        conn.send(

            b"login: "

        )

        username = conn.recv(1024).decode(

            errors="ignore"

        ).strip()

        conn.send(

            b"password: "

        )

        password = conn.recv(1024).decode(

            errors="ignore"

        ).strip()

        print(

            f"[LOGIN ATTEMPT] {ip} -> {username}:{password}"

        )

        dashboard_data["login_attempts"].append({

            "username": username,

            "password": password

        })

        conn.send(

            b"\nLast login: Thu May 22 10:15:02 2025\n"

        )

        conn.send(

            b"Welcome to Ubuntu Server\n$ "

        )
        while True:

            data = conn.recv(1024)

            if not data:

                break

            cmd = data.decode(

                errors="ignore"

            ).strip()

            if cmd == "":

                continue

            print(

                f"[ATTACK CMD] {ip} -> {cmd}"

            )

            # ------------------------------------
            # STORE COMMAND
            # ------------------------------------

            session.add_command(cmd)

            log_command(

                log_file,

                ip,

                cmd

            )

            dashboard_data["commands"].append(cmd)

            # ------------------------------------
            # ANALYZE ENTIRE SESSION
            # ------------------------------------

            result = analyze_session(

                session.commands

            )

            dashboard_data["severity"] = result["severity"]

            dashboard_data["attack_type"] = result["attack_type"]

            dashboard_data["score"] = result["score"]

            print(

                f"[SEVERITY] {result['severity']}"

            )

            print(

                f"[ATTACK TYPE] {result['attack_type']}"

            )

            print(

                f"[RISK SCORE] {result['score']}"

            )

            # ------------------------------------
            # TERMINAL LOG
            # ------------------------------------

            current_time = datetime.now().strftime(

                "%H:%M:%S"

            )

            dashboard_data["command_log"].append({

                "time": current_time,

                "command": cmd,

                "classification": result["attack_type"]

            })

            # ------------------------------------
            # GRAPH DATA
            # ------------------------------------

            dashboard_data["timeline"].append(

                len(session.commands)

            )

            # ------------------------------------
            # SEND RESPONSE
            # ------------------------------------

            response = fake_shell_response(cmd)

            conn.send(

                response.encode()

            )

            if cmd.lower() == "exit":

                break

    except Exception as e:

        print(f"[ERROR] {e}")

    finally:

        conn.close()

        # ------------------------------------
        # ALLOW NEXT ATTACKER
        # ------------------------------------

        with session_lock:

            active_session = False

        print(f"[-] Connection closed: {ip}")


# ======================================================
# SERVER
# ======================================================

def start_server():

    server = socket.socket(

        socket.AF_INET,

        socket.SOCK_STREAM

    )

    server.setsockopt(

        socket.SOL_SOCKET,

        socket.SO_REUSEADDR,

        1

    )

    server.bind(

        (HOST, PORT)

    )

    server.listen(5)

    print("\n===================================")

    print("      HONEYPOT SERVER ACTIVE")

    print("===================================\n")

    print(f"[+] Listening on {HOST}:{PORT}")

    print("[+] Maximum one attacker session allowed")

    print("[+] Waiting for attackers...\n")

    while True:

        conn, addr = server.accept()

        thread = threading.Thread(

            target=handle_client,

            args=(conn, addr)

        )

        thread.daemon = True

        thread.start()


if __name__ == "__main__":

    start_server()