from flask import Flask, request, session, redirect
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "atheer-369-secret"

DB = "atheer.db"

# ================== قاعدة البيانات ==================
def init_db():
    conn = sqlite3.connect(DB)
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

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_pass(password)))
        conn.commit()
    except:
        pass
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_pass(password)))
    user = c.fetchone()
    conn.close()
    return user

# تشغيل قاعدة البيانات
init_db()

# ================== الصفحة الرئيسية ==================
@app.route("/")
def home():
    return """
    <h1>ATHEER 369 SYSTEM</h1>
    <a href='/register'>Register</a> |
    <a href='/login'>Login</a> |
    <a href='/dashboard'>Dashboard</a> |
    <a href='/admin'>Admin</a>
    """

# ================== تسجيل ==================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        add_user(username, password)
        return redirect("/login")

    return """
    <h2>Register</h2>
    <form method="POST">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button>Register</button>
    </form>
    """

# ================== دخول ==================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = check_user(username, password)

        if user:
            session["user"] = username
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

# ================== داشبورد ==================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return f"""
    <h1>Welcome {session['user']}</h1>
    <p>Dashboard Active 🟢</p>
    <a href='/logout'>Logout</a>
    """

# ================== Admin بسيط ==================
@app.route("/admin")
def admin():
    if session.get("user") != "admin":
        return "Access Denied ❌"

    return """
    <h1>ADMIN CONTROL ROOM</h1>
    <p>System Status: RUNNING 🟢</p>
    """

# ================== خروج ==================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================== تشغيل ==================
if __name__ == "__main__":
    app.run(debug=True)

add_user("admin", "1234")
