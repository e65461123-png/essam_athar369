from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "atheer-platform"

# ================= USERS =================
users = {
    "admin": "1234",
    "Essam369": "369369"
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

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]

    return render_template("dashboard.html", user=user, balance=369.0)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
