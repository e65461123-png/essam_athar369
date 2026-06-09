from flask import Flask, render_template_string, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_key_123"

# =====================
# DATABASE SETUP
# =====================
def init_db():
    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        balance REAL DEFAULT 0
    )
    """)

    # مستخدم افتراضي
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
<p>{{ error }}</p>
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("wallet.db")
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
# HOME (WALLET)
# =====================
HOME_HTML = """
<h2>مرحباً {{ user }}</h2>
<p>رصيدك الحالي: USD {{ balance }}</p>

<a href="/logout">Logout</a>
"""

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("wallet.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE username=?", (session["user"],))
    balance = c.fetchone()[0]
    conn.close()

    return render_template_string(HOME_HTML, user=session["user"], balance=balance)

# =====================
# LOGOUT
# =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
