import socket
import threading
from datetime import datetime

from honeypot.session import Session
from honeypot.classifier import classify_attack
from logger.logger import create_session_log, log_command

HOST = "0.0.0.0"
PORT = 2222

# LIVE DASHBOARD DATA
dashboard_data = {

    "ip": "",
    "commands": [],
    "classification": "",
    "timeline": [],
    "login_attempts": [],
    "session_start": ""
}


def fake_shell_response(cmd):

    cmd = cmd.lower()

    if cmd == "ls":

        return (
            "Documents  Downloads  secret.txt  passwords.txt\n$ "
        )

    elif cmd == "pwd":

        return "/home/admin\n$ "

    elif cmd == "whoami":

        return "admin\n$ "

    elif cmd == "uname -a":

        return (
            "Linux ubuntu 5.15.0-84-generic x86_64 GNU/Linux\n$ "
        )

    elif "cat" in cmd:

        return "Permission denied\n$ "

    elif "sudo" in cmd:

        return (
            "[sudo] password for admin:\n"
            "Sorry, try again.\n$ "
        )

    elif "wget" in cmd or "curl" in cmd:

        return (
            "Connecting...\n"
            "Download failed.\n$ "
        )

    elif "nmap" in cmd:

        return (
            "Starting Nmap scan...\n"
            "Host seems down.\n$ "
        )

    elif "rm -rf" in cmd:

        return (
            "rm: dangerous operation blocked\n$ "
        )

    elif cmd == "exit":

        return "logout\n"

    else:

        return f"bash: {cmd}: command not found\n$ "


def handle_client(conn, addr):

    ip = addr[0]

    print(f"\n[+] Connection received from {ip}")

    # CREATE SESSION
    session = Session(ip)

    # CREATE LOG FILE
    log_file = create_session_log(session.id)

    # RESET DASHBOARD FOR NEW SESSION
    dashboard_data["ip"] = ip
    dashboard_data["commands"] = []
    dashboard_data["classification"] = ""
    dashboard_data["timeline"] = []
    dashboard_data["login_attempts"] = []
    dashboard_data["session_start"] = str(datetime.now())

    try:

        # FAKE SSH BANNER
        conn.send(
            b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\n"
        )

        # USERNAME
        conn.send(b"login: ")

        username = conn.recv(1024).decode(
            errors="ignore"
        ).strip()

        # PASSWORD
        conn.send(b"password: ")

        password = conn.recv(1024).decode(
            errors="ignore"
        ).strip()

        print(
            f"[LOGIN ATTEMPT] "
            f"{ip} -> {username}:{password}"
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

            print(f"[ATTACK CMD] {ip} -> {cmd}")

            # STORE COMMAND
            session.add_command(cmd)

            # LOG COMMAND
            log_command(log_file, ip, cmd)

            # UPDATE DASHBOARD
            dashboard_data["commands"].append(cmd)

            dashboard_data["timeline"].append(

                len(session.commands)
            )

            # CLASSIFY ATTACK
            classification = classify_attack(

                session.commands
            )

            dashboard_data["classification"] = (

                classification
            )

            print(
                f"[CLASSIFICATION] "
                f"{classification}"
            )

            # FAKE TERMINAL RESPONSE
            response = fake_shell_response(cmd)

            conn.send(response.encode())

            # EXIT SESSION
            if cmd.lower() == "exit":
                break

    except Exception as e:

        print(f"[ERROR] {e}")

    finally:

        conn.close()

        print(f"[-] Connection closed: {ip}")


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

    server.bind((HOST, PORT))

    server.listen(5)

    print("\n===================================")
    print("      HONEYPOT SERVER ACTIVE")
    print("===================================\n")

    print(f"[+] Listening on 0.0.0.0:{PORT}")
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