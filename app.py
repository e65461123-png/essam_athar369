from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = "ATHEER_369_ULTIMATE_KEY"

# بيانات الدخول الرسمية
ADMIN_USER = "Essam369"
ADMIN_PASSWORD = "369369"

# التصميم العسكري الرقمي (CSS)
STYLE = """
<style>
    body { background: #000; color: #0f0; font-family: 'Courier New', monospace; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
    .card { border: 1px solid #0f0; padding: 25px; width: 320px; text-align: center; box-shadow: 0 0 20px #0f0; border-radius: 10px; }
    input { width: 100%; padding: 12px; margin: 10px 0; background: #111; border: 1px solid #0f0; color: #0f0; box-sizing: border-box; }
    button { width: 100%; padding: 12px; background: #0f0; color: #000; border: none; font-weight: bold; cursor: pointer; transition: 0.3s; }
    button:hover { background: #fff; }
    .radar { width: 150px; height: 150px; border: 2px solid #0f0; border-radius: 50%; margin: 20px auto; position: relative; display: flex; align-items: center; justify-content: center; }
    .status { color: #0f0; font-size: 0.9em; margin-bottom: 15px; text-transform: uppercase; }
</style>
"""

# صفحة تسجيل الدخول
LOGIN_PAGE = f"""
<!DOCTYPE html><html><head><title>Login | ATHEER 369</title>{STYLE}</head>
<body><div class="card">
    <h1>ATHEER 369</h1>
    <form method="post">
        <input name="username" placeholder="اسم المستخدم" required>
        <input name="password" type="password" placeholder="كلمة المرور" required>
        <button type="submit">دخول إلى غرفة القيادة</button>
    </form>
</div></body></html>
"""

# صفحة غرفة العمليات (لوحة التحكم)
DASHBOARD = f"""
<!DOCTYPE html><html><head><title>Control Center | ATHEER 369</title>{STYLE}</head>
<body><div class="card" style="width: 350px;">
    <h1>ATHEER 369</h1>
    <div class="status">SYSTEM STATUS: ● ONLINE</div>
    <div class="radar">369</div>
    <div style="text-align: right; border: 1px solid #0f0; padding: 15px; margin-bottom: 15px; font-size: 0.9em;">
        <p>القائد: عصام الكومي</p>
        <p>رصيد المحفظة: USD 369.00</p>
        <p>الزوار الآن: 0007</p>
    </div>
    <button>تفعيل بوابة التدفق المالي</button><br><br>
    <button>مراسلة غرفة القيادة (GMAIL)</button><br><br>
    <a href="/logout" style="color: #f00; text-decoration: none;">تسجيل خروج</a>
</div></body></html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        return "بيانات خطأ! <a href='/'>رجوع</a>"
    return render_template_string(LOGIN_PAGE)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"): return redirect("/")
    return render_template_string(DASHBOARD)

@app.route("/logout")
def logout(): session.clear(); return redirect("/")

if __name__ == "__main__": app.run()
