from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "ATHEER_369_SECRET"

# ======================
# DATABASE INIT
# ======================
def init_db():
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ======================
# HOME
# ======================
@app.route("/")
def home():
    return render_template("index.html")

# ======================
# REGISTER
# ======================
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("platform.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?,?)",
                  (username, password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ======================
# LOGIN
# ======================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("platform.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        user = c.fetchone()

        if user and check_password_hash(user[0], password):
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")

# ======================
# DASHBOARD
# ======================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])

# ======================
# ADMIN PANEL
# ======================
@app.route("/admin")
def admin():
    if session.get("user") != "admin":
        return "Access Denied"

    return render_template("admin.html")

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
