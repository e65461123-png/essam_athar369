from flask import Flask, request, redirect, session, render_template_string
import sqlite3
import bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"

ADMIN_CODE = "369369"

# =====================
# DB INIT
# =====================
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        balance REAL DEFAULT 100.0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        type TEXT,
        amount REAL,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =====================
def add_transaction(username, type_, amount):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO transactions (username, type, amount, time) VALUES (?, ?, ?, ?)",
        (username, type_, amount, str(datetime.now()))
    )
    conn.commit()
    conn.close()

# =====================
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# =====================
# REGISTER (HASH PASSWORD)
# =====================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hashed))
            conn.commit()
        except:
            return "❌ المستخدم موجود بالفعل"
        conn.close()

        return redirect("/login")

    return render_template_string("""
    <h2>Register</h2>
    <form method="post">
        <input name="username" placeholder="Username"><br>
        <input name="password" type="password" placeholder="Password"><br>
        <button>Register</button>
    </form>
    """)

# =====================
# LOGIN
# =====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode()

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        data = c.fetchone()
        conn.close()

        if data and bcrypt.checkpw(password, data[0]):
            session["user"] = username
            return redirect("/dashboard")

        return "❌ بيانات غير صحيحة"

    return """
    <h2>Login</h2>
    <form method="post">
        <input name="username"><br>
        <input name="password" type="password"><br>
        <button>Login</button>
    </form>
    """

# =====================
# DASHBOARD
# =====================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE username=?", (user,))
    balance = c.fetchone()[0]

    c.execute("SELECT type, amount, time FROM transactions WHERE username=? ORDER BY id DESC",
              (user,))
    logs = c.fetchall()

    conn.close()

    return render_template_string("""
    <h1>👤 {{user}}</h1>
    <h3>💰 Balance: {{balance}}$</h3>

    <h3>💳 Deposit</h3>
    <form method="post" action="/deposit">
        <input name="amount" type="number">
        <button>Deposit</button>
    </form>

    <h3>💸 Withdraw</h3>
    <form method="post" action="/withdraw">
        <input name="amount" type="number">
        <button>Withdraw</button>
    </form>

    <h3>📜 Transactions</h3>
    {% for t in logs %}
        <p>{{t[0]}} | {{t[1]}}$ | {{t[2]}}</p>
    {% endfor %}

    <br>
    <a href="/admin">Admin</a> |
    <a href="/logout">Logout</a>
    """, user=user, balance=balance, logs=logs)

# =====================
# DEPOSIT
# =====================
@app.route("/deposit", methods=["POST"])
def deposit():
    user = session["user"]
    amount = float(request.form["amount"])

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE username=?",
              (amount, user))
    conn.commit()
    conn.close()

    add_transaction(user, "DEPOSIT", amount)

    return redirect("/dashboard")

# =====================
# WITHDRAW
# =====================
@app.route("/withdraw", methods=["POST"])
def withdraw():
    user = session["user"]
    amount = float(request.form["amount"])

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT balance FROM users WHERE username=?", (user,))
    balance = c.fetchone()[0]

    if amount > balance:
        return "❌ رصيد غير كافي"

    c.execute("UPDATE users SET balance = balance - ? WHERE username=?",
              (amount, user))
    conn.commit()
    conn.close()

    add_transaction(user, "WITHDRAW", amount)

    return redirect("/dashboard")

# =====================
# ADMIN
# =====================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["code"] != ADMIN_CODE:
            return "❌ Wrong code"

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT username, balance FROM users")
        users = c.fetchall()
        conn.close()

        return render_template_string("""
        <h2>🛠 Admin Panel</h2>
        {% for u in users %}
            <p>{{u[0]}} - {{u[1]}}$</p>
        {% endfor %}
        <a href="/dashboard">Back</a>
        """, users=users)

    return """
    <form method="post">
        <input name="code" placeholder="Admin Code">
        <button>Enter</button>
    </form>
    """

# =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =====================
if __name__ == "__main__":
    app.run(debug=True)
