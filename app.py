from flask import Flask, request, jsonify, session, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret-key-change-me"
DB = "wallet.db"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        balance REAL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HELPERS ----------------
def get_user(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" in session:
        user = get_user(session["user"])
        return render_template_string("""
        <h2>🚀 مرحباً {{user[1]}}</h2>
        <p>💰 الرصيد: {{user[3]}}</p>

        <a href="/logout">Logout</a>

        <hr>
        <form method="post" action="/add">
            <input name="amount" placeholder="إضافة رصيد">
            <button>إضافة</button>
        </form>

        <form method="post" action="/transfer">
            <input name="to" placeholder="المستلم">
            <input name="amount" placeholder="المبلغ">
            <button>تحويل</button>
        </form>
        """, user=user)

    return """
    <h2>🔐 Login</h2>
    <form method="post" action="/login">
        <input name="username" placeholder="username">
        <input name="password" placeholder="password">
        <button>Login</button>
    </form>

    <h3>Register</h3>
    <form method="post" action="/register">
        <input name="username">
        <input name="password">
        <button>Register</button>
    </form>
    """

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    u = request.form["username"]
    p = request.form["password"]

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, 100)", (u, p))
        conn.commit()
    except:
        return "User exists"

    conn.close()
    return redirect("/")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    u = request.form["username"]
    p = request.form["password"]

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    user = c.fetchone()
    conn.close()

    if user:
        session["user"] = u
        return redirect("/")
    return "Invalid login"

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- ADD MONEY ----------------
@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return redirect("/")

    amount = float(request.form["amount"])
    u = session["user"]

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE username=?", (amount, u))
    conn.commit()
    conn.close()

    return redirect("/")

# ---------------- TRANSFER ----------------
@app.route("/transfer", methods=["POST"])
def transfer():
    if "user" not in session:
        return redirect("/")

    sender = session["user"]
    receiver = request.form["to"]
    amount = float(request.form["amount"])

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT balance FROM users WHERE username=?", (sender,))
    sb = c.fetchone()[0]

    if sb < amount:
        return "❌ رصيد غير كافي"

    c.execute("UPDATE users SET balance = balance - ? WHERE username=?", (amount, sender))
    c.execute("UPDATE users SET balance = balance + ? WHERE username=?", (amount, receiver))

    conn.commit()
    conn.close()

    return redirect("/")

# ---------------- ADMIN API ----------------
@app.route("/api/users")
def users():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT username, balance FROM users")
    data = c.fetchall()
    conn.close()

    return jsonify(data)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
