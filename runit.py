from threading import Thread

from honeypot.server import start_server
from dashboard.app import app

server_thread = Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
