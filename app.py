from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "atheer-platform"

users = {
    "admin": "1234",
    "Essam": "369369"
}

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
