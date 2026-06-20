from flask import Flask, render_template, send_file
from reportlab.pdfgen import canvas

import io
import os

from honeypot.server import dashboard_data

app = Flask(__name__)


@app.route("/")
def index():

    safe_data = {

        "ip": dashboard_data.get("ip", ""),

        "commands": dashboard_data.get("commands", []),

        "classification": dashboard_data.get("classification", ""),

        "timeline": dashboard_data.get("timeline", [])
    }

    return render_template(
        "index.html",
        data=safe_data
    )


@app.route("/report")
def report():

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)

    p.drawString(100, 800, "HONEYPOT ATTACK REPORT")

    p.drawString(100, 770, f"Attacker IP: {dashboard_data['ip']}")

    p.drawString(100, 740, f"Classification: {dashboard_data['classification']}")

    y = 700

    p.drawString(100, y, "Commands:")

    y -= 30

    for cmd in dashboard_data["commands"]:

        p.drawString(120, y, cmd)

        y -= 20

    p.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="attack_report.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)