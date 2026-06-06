@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # تأكد إن المستخدم موجود والباسورد صح
        if username in users:
            if users[username] == password:
                session["user"] = username
                return redirect("/dashboard")

        return "Login Failed ❌"

    return render_template("login.html")
