from flask import Flask, session

app = Flask(__name__)
app.secret_key = "atheer-secret"

@app.route("/")
def home():
    return "ATHEER 369 SYSTEM WORKING 🟢"

@app.route("/admin")
def admin():
    if session.get("user") != "admin":
        return "Access Denied ❌"

    return """
    <h1>ADMIN CONTROL ROOM</h1>
    <p>System Status: RUNNING 🟢</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
