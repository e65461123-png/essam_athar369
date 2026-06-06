from flask import Flask, request, session, redirect

app = Flask(__name__)
app.secret_key = "atheer-secret-key"

# ---- صفحة الرئيسية ----
@app.route("/")
def home():
    return """
    <h1>ATHEER 369</h1>
    <a href='/login'>دخول</a> |
    <a href='/register'>تسجيل</a> |
    <a href='/dashboard'>لوحة التحكم</a>
    """

# ---- تسجيل ----
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        session["user"] = username
        session["pass"] = password

        return redirect("/login")

    return """
    <h2>Register</h2>
    <form method='POST'>
        <input name='username' placeholder='Username'>
        <input name='password' type='password' placeholder='Password'>
        <button>تسجيل</button>
    </form>
    """

# ---- دخول ----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        if user == session.get("user") and pwd == session.get("pass"):
            session["logged"] = True
            return redirect("/dashboard")

        return "بيانات غلط ❌"

    return """
    <h2>Login</h2>
    <form method='POST'>
        <input name='username'>
        <input name='password' type='password'>
        <button>دخول</button>
    </form>
    """

# ---- داشبورد ----
@app.route("/dashboard")
def dashboard():
    if not session.get("logged"):
        return redirect("/login")

    return f"""
    <h1>مرحباً {session.get('user')}</h1>
    <p>أنت داخل النظام 🟢</p>
    <a href='/logout'>خروج</a>
    """

# ---- خروج ----
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---- تشغيل ----
if __name__ == "__main__":
    app.run(debug=True)
