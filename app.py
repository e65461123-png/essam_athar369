from flask import Flask, render_template, request, session, redirect
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "atheer-super-key"

DB = "atheer.db"

# ================= HASH =================
def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ================= DATABASE =================
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

    # create admin if not exists
    c.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", hash_pass("1234"), "admin")
        )

    conn.commit()
    conn.close()

# ================= USER FUNCTIONS =================
def add_user(u, p):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (u, hash_pass(p))
        )
        conn.commit()
    except:
        pass
    conn.close()

def login_check(u, p):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (u, hash_pass(p))
    )
    user = c.fetchone()
    conn.close()
    return user

init_db()

# ================= ROUTES =================

@app.route("/")
def home():
    return redirect("/login")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        add_user(request.form["username"], request.form["password"])
        return redirect("/login")

    return """
    <h2>Register</h2>
    <form method="POST">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button>Register</button>
    </form>
    """

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = login_check(
            request.form["username"],
            request.form["password"]
        )

        if user:
            session["user"] = user[1]
            session["role"] = user[3]
            return redirect("/dashboard")

        return "Login Failed ❌"

    return """
    <h2>Login</h2>
    <form method="POST">
        <input name="username">
        <input name="password" type="password">
        <button>Login</button>
    </form>
    """

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return f"""
    <h1>Welcome {session['user']}</h1>
    <p>Dashboard Active 🟢</p>
    <a href='/logout'>Logout</a>
    """

# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access Denied ❌"

    return f"""
    <h1>ADMIN CONTROL ROOM</h1>
    <p>System Status: RUNNING 🟢</p>
    <p>Admin: {session.get('user')}</p>
    """

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
