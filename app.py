from flask import Flask, render_template_string, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret_key_123"

DB_NAME = "wallet.db"

# =====================
# INIT DATABASE
# =====================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        balance REAL DEFAULT 0
    )
    """)

    c.execute("INSERT OR IGNORE INTO users (username, password, balance) VALUES (?, ?, ?)",
              ("admin", "1234", 369.0))

    conn.commit()
    conn.close()

init_db()

# =====================
# LOGIN PAGE
# =====================
LOGIN_HTML = """
<h2>Login</h2>
<form method="POST">
    <input name="username" placeholder="Username"><br><br>
    <input name="password" type="password" placeholder="Password"><br><br>
    <button type="submit">Login</button>
</form>
<p style="color:red;">{{ error }}</p>
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            error = "بيانات غير صحيحة"

    return render_template_string(LOGIN_HTML, error=error)

# =====================
# HOME PAGE
# =====================
HOME_HTML = """
<h2>مرحباً {{ user }}</h2>
<p>رصيدك: USD {{ balance }}</p>

<h3>إدارة الرصيد</h3>

<form method="POST" action="/update_balance">
    <input name="amount" type="number" step="0.01" placeholder="المبلغ" required>
    <button name="action" value="deposit">إيداع</button>
    <button name="action" value="withdraw">سحب</button>
</form>

<br>
<a href="/logout">Logout</a>
"""

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE username=?", (session["user"],))
    balance = c.fetchone()[0]
    conn.close()

    return render_template_string(HOME_HTML, user=session["user"], balance=balance)

# =====================
# UPDATE BALANCE (داخل دالة صح)
# =====================
@app.route("/update_balance", methods=["POST"])
def update_balance():
    if "user" not in session:
        return redirect("/login")

    try:
        amount = float(request.form["amount"])
    except:
        return "مبلغ غير صحيح"

    action = request.form["action"]

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT balance FROM users WHERE username=?", (session["user"],))
    balance = c.fetchone()[0]

    if action == "deposit":
        balance += amount
    elif action == "withdraw":
        if balance >= amount:
            balance -= amount
        else:
            return "رصيد غير كافي"
    else:
        return "عملية غير صحيحة"

    c.execute("UPDATE users SET balance=? WHERE username=?", (balance, session["user"]))
    conn.commit()
    conn.close()

    return redirect("/")

# =====================
# LOGOUT
# =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =====================
# RUN
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
