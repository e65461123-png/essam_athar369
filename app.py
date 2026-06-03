from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = "ATHEER_369_PRO_SECURE"

# بيانات الدخول (يمكنك تغييرها)
ADMIN_USER = "Essam369"
ADMIN_PASSWORD = "369369"

# التصميم العام (واجهة عصرية)
STYLE = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    body { background: #0a0a0a; color: #fff; font-family: 'Segoe UI', sans-serif; }
    .glass { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .btn-gradient { background: linear-gradient(45deg, #6a11cb, #2575fc); color: white; border: none; padding: 10px 25px; border-radius: 10px; }
    .nav-icon { font-size: 1.5rem; margin-bottom: 10px; color: #00d4ff; }
</style>
"""

# صفحة تسجيل الدخول
LOGIN_PAGE = f"""
<!DOCTYPE html><html><head><title>ATHEER 369 | Login</title>{STYLE}</head>
<body class="d-flex justify-content-center align-items-center vh-100">
    <div class="glass text-center" style="width: 350px;">
        <i class="fas fa-rocket nav-icon"></i>
        <h3>ATHEER 369</h3>
        <form method="post" class="mt-4">
            <input name="username" class="form-control bg-dark text-white border-0 mb-3" placeholder="اسم المستخدم" required>
            <input name="password" type="password" class="form-control bg-dark text-white border-0 mb-3" placeholder="كلمة المرور" required>
            <button type="submit" class="btn btn-gradient w-100">دخول المنصة</button>
        </form>
    </div>
</body></html>
"""

# غرفة العمليات (لوحة الإدارة)
DASHBOARD = f"""
<!DOCTYPE html><html><head><title>ATHEER 369 | Control Center</title>{STYLE}</head>
<body class="p-4">
    <div class="container-fluid">
        <div class="d-flex justify-content-between align-items-center mb-5">
            <h2><i class="fas fa-terminal"></i> غرفة العمليات</h2>
            <a href="/logout" class="btn btn-danger">تسجيل خروج</a>
        </div>
        <div class="row">
            <div class="col-md-4"><div class="glass text-center"><i class="fas fa-users nav-icon"></i><h4>المستخدمين</h4><p>1,240</p></div></div>
            <div class="col-md-4"><div class="glass text-center"><i class="fas fa-server nav-icon"></i><h4>حالة السيرفر</h4><p>نشط 100%</p></div></div>
            <div class="col-md-4"><div class="glass text-center"><i class="fas fa-shield-alt nav-icon"></i><h4>الحماية</h4><p>مفعلة (Secure)</p></div></div>
        </div>
    </div>
</body></html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        return "بيانات خطأ!"
    return render_template_string(LOGIN_PAGE)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"): return redirect("/")
    return render_template_string(DASHBOARD)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
