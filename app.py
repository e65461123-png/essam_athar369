from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
# قم بتغيير هذه المفتاح السري لشيء خاص بك
app.secret_key = "ATHEER_369_SUPER_SECURE_KEY_2026"

# كلمة المرور الخاصة بلوحة التحكم
ADMIN_PASSWORD = "your_secure_password_here" 

# التصميم والمظهر (Glassmorphism UI)
THEME = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    body { background: #050505; color: #fff; font-family: 'Cairo', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .glass { background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 25px; backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.1); text-align: center; width: 350px; box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37); }
    input { width: 100%; padding: 15px; margin: 15px 0; border-radius: 12px; border: none; background: rgba(0,0,0,0.3); color: white; box-sizing: border-box; outline: none; border: 1px solid #444; }
    button { width: 100%; padding: 15px; background: linear-gradient(135deg, #6a00ff, #ff007f); border: none; border-radius: 12px; color: white; cursor: pointer; font-weight: bold; font-size: 16px; transition: 0.3s; }
    button:hover { transform: scale(1.05); }
    h1 { margin-bottom: 20px; letter-spacing: 2px; }
</style>
"""

LOGIN_HTML = f"""
<!DOCTYPE html><html dir="rtl"><head><title>Login | ATHEER 369</title>{THEME}</head>
<body><div class="glass">
    <h1>🚀 ATHEER 369</h1>
    <form method="post"><input name="password" type="password" placeholder="أدخل كلمة المرور" required>
    <button type="submit">دخول إلى المنصة</button></form>
</div></body></html>
"""

DASHBOARD_HTML = f"""
<!DOCTYPE html><html dir="rtl"><head><title>Dashboard | ATHEER 369</title>{THEME}</head>
<body><div class="glass" style="width: 500px;">
    <h1>مرحباً بك في المركز الرئيسي</h1>
    <p style="color: #00ffaa; font-size: 1.2em;">النظام يعمل بكامل قوته 🟢</p>
    <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin: 20px 0;">
        <p>إجمالي المستخدمين: 1,240</p>
        <p>حالة الخادم: مستقر</p>
    </div>
    <a href="/logout"><button style="background: #ff4444;">تسجيل الخروج</button></a>
</div></body></html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        return "كلمة مرور خاطئة! <a href='/'>رجوع</a>"
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
