import subprocess
import time

print("\n===================================")
print("   HONEYPOT ATTACK FRAMEWORK")
print("===================================\n")

print("[+] Starting Honeypot Server...")
print("[+] Listening on port 2222")
print("[+] Waiting for attackers...\n")

print("[!] Press CTRL + C to stop\n")

# START HONEYPOT
honeypot = subprocess.Popen(
    ["python3", "-m", "honeypot.server"]
)

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    print("\n[-] Stopping Honeypot...")

    honeypot.terminate()

    print("[+] Honeypot stopped successfully\n")
