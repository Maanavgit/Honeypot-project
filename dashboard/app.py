from flask import Flask, render_template, send_file
from reportlab.pdfgen import canvas

from collections import Counter
from datetime import datetime, timedelta

import io

from honeypot.server import dashboard_data

app = Flask(__name__)


@app.route("/")
def index():

    # =====================================================
    # BUILD GRAPH DATA (COMMANDS PER MINUTE)
    # =====================================================

    command_log = dashboard_data.get(

        "command_log",

        []

    )

    time_counter = Counter()

    for item in command_log:

        minute = item["time"][:5]

        time_counter[minute] += 1

    graph_labels = []

    graph_values = []

    if time_counter:

        sorted_minutes = sorted(

            time_counter.keys()

        )

        start = datetime.strptime(

            sorted_minutes[0],

            "%H:%M"

        )

        end = datetime.strptime(

            sorted_minutes[-1],

            "%H:%M"

        )

        current = start

        while current <= end:

            minute = current.strftime(

                "%H:%M"

            )

            graph_labels.append(

                minute

            )

            graph_values.append(

                time_counter.get(

                    minute,

                    0

                )

            )

            current += timedelta(

                minutes=1

            )

    # =====================================================
    # SEND DATA TO TEMPLATE
    # =====================================================

    safe_data = {

        "ip":

            dashboard_data.get(

                "ip",

                ""

            ),

        "severity":

            dashboard_data.get(

                "severity",

                "LOW"

            ),

        "commands":

            dashboard_data.get(

                "commands",

                []

            ),

        "command_log":

            command_log,

        "graph_labels":

            graph_labels,

        "graph_values":

            graph_values,

        "session_start":

            dashboard_data.get(

                "session_start",

                ""

            ),

        "total_commands":

            len(

                dashboard_data.get(

                    "commands",

                    []

                )

            )

    }

    return render_template(

        "index.html",

        data=safe_data

    )


# =====================================================
# PDF REPORT
# =====================================================

@app.route("/report")
def report():

    buffer = io.BytesIO()

    pdf = canvas.Canvas(

        buffer

    )

    pdf.setTitle(

        "Honeypot Attack Report"

    )

    pdf.setFont(

        "Helvetica-Bold",

        18

    )

    pdf.drawString(

        60,

        810,

        "HONEYPOT ATTACK REPORT"

    )

    pdf.setFont(

        "Helvetica",

        12

    )

    pdf.drawString(

        60,

        780,

        f"Source IP : {dashboard_data.get('ip','-')}"

    )

    pdf.drawString(

        60,

        760,

        f"Threat Severity : {dashboard_data.get('severity','LOW')}"

    )

    pdf.drawString(

        60,

        740,

        f"Session Started : {dashboard_data.get('session_start','-')}"

    )

    pdf.drawString(

        60,

        720,

        f"Commands Captured : {len(dashboard_data.get('commands', []))}"

    )

    y = 680

    pdf.setFont(

        "Helvetica-Bold",

        13

    )

    pdf.drawString(

        60,

        y,

        "Captured Commands"

    )

    y -= 25

    pdf.setFont(

        "Helvetica",

        11

    )

    command_log = dashboard_data.get(

        "command_log",

        []

    )

    if command_log:

        for item in command_log:

            line = (

                f"[{item['time']}] "

                f"{item['command']}"

            )

            pdf.drawString(

                70,

                y,

                line

            )

            y -= 18

            if y < 60:

                pdf.showPage()

                pdf.setFont(

                    "Helvetica",

                    11

                )

                y = 800

    else:

        pdf.drawString(

            70,

            y,

            "No commands captured."

        )

    pdf.save()

    buffer.seek(0)
    
    return send_file(

        buffer,

        as_attachment=True,

        download_name="attack_report.pdf",

        mimetype="application/pdf"

    )


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
