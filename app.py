from flask import Flask, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "aether_secret"

DB = "aether.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        balance INTEGER DEFAULT 0
    )
    """)

    # admin hashed password
    hashed = generate_password_hash("1234")

    c.execute("""
    INSERT OR IGNORE INTO users (username, password, balance)
    VALUES (?, ?, ?)
    """, ("admin", hashed, 1000))

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")

        conn = get_db()
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=?", (u,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], p):
            session["user"] = u
            return redirect("/dashboard")

        return "❌ بيانات غير صحيحة"

    return """
    <h2>AETHER LOGIN</h2>
    <form method="post">
        <input name="username" placeholder="username">
        <input name="password" type="password" placeholder="password">
        <button>Login</button>
    </form>
    """


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT balance FROM users WHERE username=?", (session["user"],))
    row = c.fetchone()
    conn.close()

    balance = row["balance"] if row else 0

    return f"""
    <h1>👤 Welcome {session['user']}</h1>
    <h3>💰 Balance: {balance}</h3>

    <form action="/topup" method="post">
        <input name="amount" placeholder="topup">
        <button>Charge</button>
    </form>

    <form action="/use" method="post">
        <input name="amount" placeholder="use">
        <button>Pay</button>
    </form>

    <a href="/logout">Logout</a>
    """


@app.route("/topup", methods=["POST"])
def topup():
    if "user" not in session:
        return redirect("/")

    try:
        amount = int(request.form.get("amount", 0))
    except:
        return "❌ رقم غير صالح"

    if amount <= 0:
        return "❌ لازم رقم أكبر من صفر"

    conn = get_db()
    c = conn.cursor()

    c.execute("UPDATE users SET balance = balance + ? WHERE username=?",
              (amount, session["user"]))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/use", methods=["POST"])
def use():
    if "user" not in session:
        return redirect("/")

    try:
        amount = int(request.form.get("amount", 0))
    except:
        return "❌ رقم غير صالح"

    if amount <= 0:
        return "❌ لازم رقم أكبر من صفر"

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT balance FROM users WHERE username=?", (session["user"],))
    bal = c.fetchone()["balance"]

    if amount > bal:
        return "❌ رصيد غير كافي"

    c.execute("UPDATE users SET balance = balance - ? WHERE username=?",
              (amount, session["user"]))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
