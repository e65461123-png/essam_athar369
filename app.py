from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "atheer-platform-key"

# 🔐 قاعدة بيانات بسيطة (مرحلة أولى)
users = {
    "admin": {
        "password": generate_password_hash("1234"),
        "role": "admin"
    }
}

@app.route("/")
def home():
    return redirect("/login")

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "User already exists ❌"

        users[username] = {
            "password": generate_password_hash(password),
            "role": "user"
        }

        return redirect("/login")

    return render_template("register.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(username)

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            session["role"] = user["role"]
            return redirect("/dashboard")

        return "Login Failed ❌"

    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user_data = {
        "name": session["user"],
        "balance": 369.00
    }

    return render_template("dashboard.html", data=user_data)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
