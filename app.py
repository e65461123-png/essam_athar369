from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- كود الواجهة الرئيسية ---
home_html = """
<div style="text-align:center; padding-top:50px; font-family:Tahoma; background:#0f172a; color:white; min-height:100vh;">
    <h1>AETHER 369</h1>
    <div style="width:300px; margin:auto; background:#1e293b; padding:20px; border-radius:15px;">
        <h3>الاسم: عصام الكومي</h3>
        <p>رصيد USD 369.00</p>
        <a href="/login" style="color:white; display:block; margin:10px; text-decoration:none;">تسجيل الدخول</a>
        <a href="/register" style="color:white; display:block; margin:10px; text-decoration:none;">إنشاء حساب جديد</a>
    </div>
</div>
"""

# --- كود صفحة تسجيل الدخول ---
login_html = """
<div style="text-align:center; padding-top:50px; font-family:Tahoma; background:#0f172a; color:white; min-height:100vh;">
    <h2>تسجيل الدخول</h2>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="اسم المستخدم" required style="padding:10px; margin:5px;"><br>
        <input type="password" name="password" placeholder="كلمة المرور" required style="padding:10px; margin:5px;"><br>
        <button type="submit" style="padding:10px 20px; margin:10px; background:#2561eb; color:white; border:none; border-radius:5px;">دخول</button>
    </form>
    <a href="/" style="color:white; text-decoration:none;">العودة للرئيسية</a>
</div>
"""

@app.route('/')
def home():
    return render_template_string(home_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # المرحلة القادمة: هنا سنربط بقاعدة البيانات لاحقاً
        return "تم استلام البيانات بنجاح! نحن جاهزون للمرحلة التالية."
    return render_template_string(login_html)

if __name__ == '__main__':
    app.run(debug=True)
