import uuid
from datetime import datetime

class Session:
    def __init__(self, ip):
        self.id = str(uuid.uuid4())[:8]
        self.ip = ip
        self.start_time = datetime.now()
        self.commands = []
        self.classification = "Unknown"

    def add_command(self, cmd):
        self.commands.append(cmd)