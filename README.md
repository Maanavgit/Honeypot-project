# Honeypot-Based Attack Monitoring Framework

A lightweight TCP socket honeypot developed in Python for monitoring attacker activities in a controlled environment. The framework simulates a Linux shell, captures attacker commands, classifies attack behavior, evaluates threat severity, logs each session, provides a real-time web dashboard, and generates downloadable PDF reports.

The application is containerized using **Docker** and can be built and deployed using **Docker Compose**.

> **Note:** This project is intended for educational purposes, cybersecurity research, and laboratory demonstrations only. Do not deploy it on public networks without proper security controls.

---

## Features

* TCP Socket-based Honeypot Server
* Simulated Linux Shell
* Rule-based Attack Classification
* Threat Severity Evaluation
* Session-wise Attack Logging
* Real-time Flask Dashboard
* Commands Per Minute Graph
* PDF Report Generation
* Single Session Management
* Docker Containerization
* Persistent Logs and Reports using Docker Volumes

---

## Technologies Used

* Python 3
* Flask
* Python Socket Programming
* Python Threading
* HTML5
* CSS3
* JavaScript
* Chart.js
* ReportLab
* Docker
* Docker Compose

---

# Project Structure

```text
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
├── runit.py
├── requirements.txt
├── Dockerfile
└── compose.yml
```

---

# Prerequisites

The project is containerized, so Python and pip do not need to be installed directly on the host.

Install:

* Docker
* Docker Compose

### Windows

Install **Docker Desktop**.

After installation, verify Docker:

```bash
docker --version
```

Verify Docker Compose:

```bash
docker compose version
```

### Linux

Install Docker and Docker Compose according to your Linux distribution.

Verify:

```bash
docker --version
docker compose version
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Maanavgit/Honeypot-project.git
```

Move into the project directory:

```bash
cd Honeypot-project
```

The project can now be built and started using Docker Compose.

---

# Docker Configuration

The project contains a `Dockerfile` used to build the application image.

Example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs reports

EXPOSE 2222
EXPOSE 5000

CMD ["python", "runit.py"]
```

The project also contains a `compose.yml` file:

```yaml
services:
  honeypot:
    build: .
    container_name: honeypot
    ports:
      - "2222:2222"
      - "5000:5000"
    volumes:
      - ./logs:/app/logs
      - ./reports:/app/reports
    restart: unless-stopped
```

The Docker container exposes:

| Host Port | Container Port | Purpose             |
| --------- | -------------: | ------------------- |
| 2222      |           2222 | Honeypot TCP server |
| 5000      |           5000 | Flask dashboard     |

The `logs` and `reports` directories are mounted as volumes so that generated data remains available on the host even if the container is recreated.

---

# Building and Running

From the project directory, run:

```bash
docker compose up -d --build
```

This command:

1. Builds the Docker image.
2. Creates the honeypot container.
3. Starts the container in detached mode.
4. Maps the required ports.
5. Mounts the logs and reports directories.

Check the running container:

```bash
docker compose ps
```

or:

```bash
docker ps
```

---

# Viewing Container Logs

To view the application output:

```bash
docker compose logs -f
```

Press:

```text
Ctrl + C
```

to stop viewing the logs.

This does not stop the container.

---

# Accessing the Dashboard

Once the container is running, open:

```text
http://127.0.0.1:5000
```

If the honeypot is running on another machine, use:

```text
http://<HONEYPOT-IP>:5000
```

Example:

```text
http://192.168.56.101:5000
```

The dashboard displays:

* Threat Severity
* Source IP
* Session Status
* Live Command Terminal
* Threat Summary
* Commands Per Minute Graph
* Download PDF Report

---

# Simulating an Attack

From another machine connected to the same network, use Netcat or Ncat.

```bash
ncat <HONEYPOT-IP> 2222
```

Example:

```bash
ncat 192.168.56.101 2222
```

After connecting, enter:

```text
login:
```

and:

```text
password:
```

The honeypot accepts the input and opens the simulated Linux shell.

Try commands such as:

```text
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

The framework captures the commands and updates the dashboard.

---

# Docker Container Management

## Start the application

```bash
docker compose start
```

## Stop the application

```bash
docker compose stop
```

## Restart the application

```bash
docker compose restart
```

## Stop and remove the container

```bash
docker compose down
```

The `logs` and `reports` directories on the host are not removed.

## Rebuild after changing source code

After modifying the Python source code, rebuild the image:

```bash
docker compose up -d --build
```

---

# Generated Files

## Logs

Every attack session creates an individual log file.

Example:

```text
logs/
└── attack_session_2026-07-26_10-30-52.log
```

The `logs` directory is mounted from the host into the container:

```text
./logs:/app/logs
```

Therefore, logs remain available even when the container is recreated.

---

## Reports

The dashboard allows downloading a PDF report containing:

* Source IP
* Threat Severity
* Session Start Time
* Total Commands
* Command Timeline

Generated reports are stored in:

```text
reports/
```

The directory is mounted into the container using:

```text
./reports:/app/reports
```

---

# Threat Severity Levels

| Severity | Criteria                                                                   |
| -------- | -------------------------------------------------------------------------- |
| LOW      | Basic reconnaissance commands such as `ls`, `pwd`, `whoami`, `uname -a`    |
| MEDIUM   | Reconnaissance and privilege enumeration such as `nmap`, `cat /etc/passwd` |
| HIGH     | Brute-force or malicious download attempts such as `hydra`, `wget`, `curl` |
| CRITICAL | Destructive commands such as `rm -rf`                                      |

The highest detected severity becomes the overall session severity.

---

# Container Architecture

```text
                    Docker Host
                         │
                         │
                ┌────────▼────────┐
                │ Honeypot        │
                │ Container       │
                │                 │
                │ Python          │
                │ Flask           │
                │ Honeypot Server │
                └───────┬─────────┘
                        │
              ┌─────────┴─────────┐
              │                   │
           Port 2222           Port 5000
              │                   │
              ▼                   ▼
        Honeypot TCP          Web Dashboard
        Connection            Browser
              
              │
              ▼
       ┌───────────────┐
       │ Host Volumes  │
       │               │
       │ ./logs        │
       │ ./reports     │
       └───────────────┘
```

---

# Notes

* Only one attacker session is allowed at a time.
* If another client connects while a session is active, the server returns:

```text
Server Busy. Please try again later.
```

* Every new session creates a new log file.
* Dashboard data resets for every new attacker session.
* Logs and reports are persisted on the host through Docker volume mappings.
* The application runs inside a Docker container and does not require a Python installation on the host.

---

# Troubleshooting

## Docker daemon is not running

If you receive an error similar to:

```text
failed to connect to the docker API
```

make sure Docker Desktop is running on Windows.

Test:

```bash
docker info
```

---

## Container is not running

Check:

```bash
docker compose ps
```

View the container logs:

```bash
docker compose logs
```

---

## Dashboard not opening

Check whether the container is running:

```bash
docker compose ps
```

Check application logs:

```bash
docker compose logs -f
```

Verify that port `5000` is available.

---

## Honeypot connection fails

Verify that port `2222` is exposed:

```bash
docker compose ps
```

The output should contain:

```text
0.0.0.0:2222->2222/tcp
```

Then connect:

```bash
ncat <HONEYPOT-IP> 2222
```

---

## Port already in use

If port `2222` or `5000` is already being used, change the host-side port in `compose.yml`.

For example:

```yaml
ports:
  - "2223:2222"
  - "5001:5000"
```

The application will still use ports `2222` and `5000` inside the container.

You would then connect using:

```bash
ncat <HONEYPOT-IP> 2223
```

and access the dashboard using:

```text
http://<HONEYPOT-IP>:5001
```

---

## Rebuild the application

If source code or dependencies have changed:

```bash
docker compose down
docker compose up -d --build
```

---

# Future Improvements

* SSH-based Honeypot
* Multi-attacker support
* Machine Learning attack classification
* Database integration
* SIEM integration
* Email alerts
* HTTP/FTP/Telnet Honeypots
* Docker-based multi-service deployment
* Centralized attack log storage

---

# Author

**T S Maanav**

MCA (Cybersecurity)

GitHub Repository:

https://github.com/Maanavgit/Honeypot-project

---

# License

This project is developed for academic and educational purposes.
