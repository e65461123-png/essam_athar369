from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = "ATHEER_369_SECURE_KEY"

# بيانات الدخول
ADMIN_USER = "Essam369"
ADMIN_PASSWORD = "369369"

# التصميم (CSS)
STYLE = """
<style>
    body { background: #050505; color: #fff; font-family: 'Arial', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .card { background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid #333; text-align: center; width: 320px; }
    input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: none; background: #222; color: white; box-sizing: border-box; }
    button { width: 100%; padding: 12px; background: linear-gradient(45deg, #6a00ff, #ff007f); border: none; border-radius: 8px; color: white; cursor: pointer; font-weight: bold; }
</style>
"""

# صفحة تسجيل الدخول
LOGIN_HTML = f"""
<!DOCTYPE html><html><head><title>Login | ATHEER 369</title>{STYLE}</head>
<body><div class="card">
    <h1>ATHEER 369</h1>
    <form method="post">
        <input name="username" placeholder="اسم المستخدم" required>
        <input name="password" type="password" placeholder="كلمة المرور" required>
        <button type="submit">دخول</button>
    </form>
</div></body></html>
"""

# لوحة التحكم
DASHBOARD_HTML = f"""
<!DOCTYPE html><html><head><title>Dashboard</title>{STYLE}</head>
<body><div class="card">
    <h1>مرحباً يا عصام</h1>
    <p>تم الدخول بنجاح إلى منصة ATHEER 369 🚀</p>
    <a href="/logout"><button style="background: #ff4444;">تسجيل الخروج</button></a>
</div></body></html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        return "بيانات خطأ! <a href='/'>حاول مرة أخرى</a>"
    return render_template_string(LOGIN_HTML)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template_string(DASHBOARD_HTML)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
