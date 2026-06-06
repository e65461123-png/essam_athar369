from flask import Flask, request, redirect, session, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "aether_secret"

DB = "aether.db"


# =====================
# DATABASE
# =====================
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

    hashed = generate_password_hash("1234")

    c.execute("""
    INSERT OR IGNORE INTO users (username, password, balance)
    VALUES (?, ?, ?)
    """, ("admin", hashed, 1000))

    conn.commit()
    conn.close()


# =====================
# LOGIN
# =====================
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
    <h2>AETHER 369 LOGIN</h2>
    <form method="post">
        <input name="username" placeholder="username">
        <input name="password" type="password" placeholder="password">
        <button>Login</button>
    </form>
    """


# =====================
# DASHBOARD (النظام الجديد)
# =====================
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

    return render_template_string(f"""
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>AETHER 369</title>

<style>
body {{
    margin:0;
    font-family:Arial;
    background:linear-gradient(120deg,#000,#111,#000);
    color:white;
    text-align:center;
}}

.card {{
    margin-top:50px;
    padding:20px;
}}

h1 {{
    color:#00ffcc;
}}

button {{
    padding:10px 20px;
    margin:5px;
    border:none;
    border-radius:8px;
    cursor:pointer;
}}

input {{
    padding:10px;
    margin:5px;
    border-radius:8px;
    border:none;
}}

.logout {{
    color:red;
    display:block;
    margin-top:20px;
}}
</style>

</head>

<body>

<div class="card">

    <h1>🔥 AETHER 369</h1>
    <h3>👑 القائد: عصام الكومي</h3>

    <hr style="width:50%">

    <h2>💰 رصيد المحفظة</h2>
    <h1>USD {balance}.00</h1>

    <form action="/topup" method="post">
        <input name="amount" placeholder="إضافة رصيد">
        <button>Charge</button>
    </form>

    <form action="/use" method="post">
        <input name="amount" placeholder="سحب رصيد">
        <button>Pay</button>
    </form>

    <a class="logout" href="/logout">Logout</a>

</div>

</body>
</html>
""")


# =====================
# TOPUP
# =====================
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


# =====================
# USE
# =====================
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


# =====================
# LOGOUT
# =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =====================
# RUN
# =====================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
