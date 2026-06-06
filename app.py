from flask import Flask, render_template, request, session, redirect
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "atheer-super-key"

DB = "atheer.db"

# ================= DB =================
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)

    # create admin
    c.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  ("admin", hash_pass("1234"), "admin"))

    conn.commit()
    conn.close()

def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

def add_user(u, p):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
              (u, hash_pass(p)))
    conn.commit()
    conn.close()

def login_check(u, p):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (u, hash_pass(p)))
    return c.fetchone()

init_db()

# ================= ROUTES =================
@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        add_user(request.form["username"], request.form["password"])
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = login_check(request.form["username"], request.form["password"])

        if user:
            session["user"] = user[1]
            session["role"] = user[3]
            return redirect("/dashboard")

        return "Login Failed ❌"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])

@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access Denied ❌"

    return render_template("admin.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
