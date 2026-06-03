from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "ATHEER369_SECRET"

LOGIN_PAGE = """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<title>ATHEER 369</title>
<style>
body{
background:#0a0a0a;
color:white;
font-family:Arial;
text-align:center;
padding:50px;
}
input{
padding:10px;
margin:5px;
width:250px;
}
button{
padding:10px 20px;
background:#6a00ff;
color:white;
border:none;
cursor:pointer;
}
</style>
</head>
<body>
<h1>🚀 ATHEER 369 PLATFORM</h1>
<form method="post">
<input name="username" placeholder="اسم المستخدم"><br>
<input name="password" type="password" placeholder="كلمة المرور"><br>
<button type="submit">دخول</button>
</form>
</body>
</html>
"""

DASHBOARD = """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<title>ATHEER 369</title>
<style>
body{
background:#111;
color:white;
font-family:Arial;
text-align:center;
}
.card{
background:#1d1d1d;
padding:20px;
margin:20px;
border-radius:15px;
}
</style>
</head>
<body>

<h1>🔥 ATHEER 369 CONTROL CENTER</h1>

<div class="card">
<h2>مرحباً {{user}}</h2>
<p>Platform Active 🟢</p>
</div>

<div class="card">
<h3>لوحة التحكم</h3>
<p>إدارة المستخدمين</p>
<p>غرفة العمليات</p>
<p>سجل النشاط</p>
</div>

<a href="/logout">
<button>تسجيل الخروج</button>
</a>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["user"] = request.form["username"]
        return redirect("/dashboard")

    return render_template_string(LOGIN_PAGE)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template_string(
        DASHBOARD,
        user=session["user"]
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
