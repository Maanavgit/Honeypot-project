# Honeypot-Based Attack Monitoring Framework

A lightweight TCP socket honeypot developed in Python for monitoring attacker activities in a controlled environment. The framework simulates a Linux shell, captures attacker commands, classifies attack behavior, evaluates threat severity, logs each session, provides a real-time web dashboard, and generates downloadable PDF reports.

> **Note:** This project is intended for educational purposes, cybersecurity research, and laboratory demonstrations only. Do not deploy it on public networks without proper security controls.

---

## Features

- TCP Socket-based Honeypot Server
- Simulated Linux Shell
- Rule-based Attack Classification
- Threat Severity Evaluation
- Session-wise Attack Logging
- Real-time Flask Dashboard
- Commands Per Minute Graph
- PDF Report Generation
- Single Session Management

---

## Technologies Used

- Python 3
- Flask
- Python Socket Programming
- Python Threading
- HTML5
- CSS3
- JavaScript
- Chart.js
- ReportLab

---

## Project Structure

```
Honeypot-project/
│
├── honeypot/
│   ├── server.py
│   ├── classifier.py
│   ├── session.py
│   └── logger.py
│
├── dashboard/
│   ├── app.py
│   ├── templates/
│   └── static/
│
├── reports/
├── logs/
├── run.py
├── honeypot.py
└── requirements.txt
```

---

# Prerequisites

Before running the project, make sure you have:

- Python 3.10 or later
- pip
- Git
- A Linux environment (Kali Linux recommended)

---

# Installation

Clone the repository

```bash
git clone https://github.com/Maanavgit/Honeypot-project.git
```

Move into the project directory

```bash
cd Honeypot-project
```

Create a virtual environment

```bash
python3 -m venv venv
```

Activate the virtual environment

```bash
source venv/bin/activate
```

Install all required packages

```bash
pip install -r requirements.txt
```

---

# Running the Project

The project has two execution modes.

## Option 1 - Honeypot Only

Run

```bash
python3 honeypot.py
```

This starts only the honeypot server.

The server listens on

```
Port 2222
```

---

## Option 2 - Honeypot + Dashboard

Run

```bash
python3 run.py
```

This starts

- Honeypot Server
- Dashboard Backend

The dashboard becomes available at

```
http://127.0.0.1:5000
```

or

```
http://<Kali-IP>:5000
```

---

# Simulating an Attack

From another machine connected to the same network, use Netcat.

Example

```bash
ncat <HONEYPOT-IP> 2222
```

Example

```bash
ncat 192.168.56.101 2222
```

After connecting

Enter

```
login:
```

and

```
password:
```

The honeypot accepts the input and opens the simulated Linux shell.

Try commands like

```
ls
pwd
whoami
uname -a
nmap
hydra
wget
curl
cat /etc/passwd
rm -rf
```

The framework captures every command and updates the dashboard automatically.

---

# Dashboard

Open a browser and visit

```
http://127.0.0.1:5000
```

The dashboard displays

- Threat Severity
- Source IP
- Session Status
- Live Command Terminal
- Threat Summary
- Commands Per Minute Graph
- Download PDF Report

---

# Generated Files

## Logs

Every attack session creates an individual log file.

Example

```
logs/
    attack_session_2026-07-26_10-30-52.log
```

---

## Reports

The dashboard allows downloading a PDF report containing

- Source IP
- Threat Severity
- Session Start Time
- Total Commands
- Command Timeline

---

# Threat Severity Levels

| Severity | Criteria |
|----------|----------|
| LOW | Basic reconnaissance commands (`ls`, `pwd`, `whoami`, `uname -a`) |
| MEDIUM | Reconnaissance and privilege enumeration (`nmap`, `cat /etc/passwd`) |
| HIGH | Brute-force or malicious download attempts (`hydra`, `wget`, `curl`) |
| CRITICAL | Destructive commands (`rm -rf`) |

The highest detected severity becomes the overall session severity.

---

# Notes

- Only one attacker session is allowed at a time.
- If another client connects while a session is active, the server returns:

```
Server Busy. Please try again later.
```

- Every new session creates a new log file.
- Dashboard data resets for every new attacker session.

---

# Troubleshooting

### Dashboard not opening

Verify Flask is running.

```bash
python3 run.py
```

---

### Port already in use

Check which process is using port 2222

```bash
sudo lsof -i :2222
```

Terminate it if necessary.

---

### Permission denied

If binding to the port fails

```bash
sudo python3 run.py
```

or change the listening port in the source code.

---

### Modules not found

Reinstall dependencies

```bash
pip install -r requirements.txt
```

---

# Future Improvements

- SSH-based Honeypot
- Multi-attacker support
- Machine Learning attack classification
- Database integration
- SIEM integration
- Email alerts
- HTTP/FTP/Telnet Honeypots

---

# Author

**T S Maanav**

MCA (Cybersecurity)

GitHub Repository

https://github.com/Maanavgit/Honeypot-project

---

# License

This project is developed for academic and educational purposes.
