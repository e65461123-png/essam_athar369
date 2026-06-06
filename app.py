from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "atheer-platform"

# ================= USERS =================
users = {
    "admin": "1234",
    "Essam": "369369"
}

# ================= HOME =================
@app.route("/")
def home():
    return redirect("/login")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/dashboard")

        return "Login Failed ❌"

    return render_template("login.html")

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            return "User already exists ❌"

        users[username] = password
        return redirect("/login")

    return render_template("register.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return f"""
    <h1>AETHER 369</h1>
    <h2>Welcome {session['user']}</h2>
    <p>Dashboard Active 🟢</p>
    <a href="/logout">Logout</a>
    """

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
