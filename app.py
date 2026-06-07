from flask import Flask, request, redirect, session, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = "secret_key_123"

ADMIN_CODE = "369369"

# =====================
# DATABASE
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
    conn.commit()
    conn.close()

init_db()

# =====================
# HOME
# =====================
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# =====================
# REGISTER
# =====================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, password))
            conn.commit()
        except:
            return "❌ Username already exists"
        conn.close()

        return redirect("/login")

    return render_template_string("""
    <h2>Register</h2>
    <form method="post">
        <input name="username" placeholder="Username"><br>
        <input name="password" type="password" placeholder="Password"><br>
        <button type="submit">Register</button>
    </form>
    <a href="/login">Login</a>
    """)

# =====================
# LOGIN
# =====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        return "❌ Invalid login"

    return render_template_string("""
    <h2>Login</h2>
    <form method="post">
        <input name="username" placeholder="Username"><br>
        <input name="password" type="password" placeholder="Password"><br>
        <button type="submit">Login</button>
    </form>
    <a href="/register">Register</a>
    """)

# =====================
# DASHBOARD
# =====================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE username=?", (username,))
    balance = c.fetchone()[0]
    conn.close()

    return render_template_string("""
    <h1>👋 Welcome {{user}}</h1>
    <h3>Balance: {{balance}} $</h3>

    <a href="/admin">Admin Panel</a><br>
    <a href="/logout">Logout</a>
    """, user=username, balance=balance)

# =====================
# ADMIN PANEL
# =====================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        code = request.form["code"]
        if code == ADMIN_CODE:
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

        return "❌ Wrong admin code"

    return """
    <h2>Admin Login</h2>
    <form method="post">
        <input name="code" placeholder="Admin Code">
        <button type="submit">Enter</button>
    </form>
    """

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
    app.run(debug=True)
