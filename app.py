from flask import Flask, render_template, session, redirect, url_for
from functools import wraps

app = Flask(__name__)
app.secret_key = 'AETHER_SECRET_369_KEY' # مفتاح تشفير الجلسات لحماية الـ Admin

# ديكوريتور (حارس) للتأكد من أن الأدمن فقط من يدخل الصفحة
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('login')) # لو مش مسجل يحوله فوراً
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # هنا هنجيب البيانات حية من قاعدة البيانات اللي صممتها (SQL Tables)
    admin_data = {
        'username': 'Admin',
        'balance': 369.00,
        'security_status': 'SAFU SECURED'
    }
    return render_template('dashboard.html', data=admin_data)

if __name__ == '__main__':
    # التشغيل محلياً أو التجهيز للرفع المباشر على Render
    app.run(debug=True, port=5000)
