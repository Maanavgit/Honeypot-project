from dashboard.app import app

print("\n==============================")
print(" DASHBOARD SERVER ")
print("==============================\n")

app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)
