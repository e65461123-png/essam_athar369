from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

# الواجهة الموحدة
layout = """
<div style="text-align:center; padding-top:50px; font-family:Tahoma; background:#0f172a; color:white; min-height:100vh;">
    <h1>AETHER 369</h1>
    <div style="width:300px; margin:auto; background:#1e293b; padding:20px; border-radius:15px;">
        {{ content | safe }}
        <br><br>
        <a href="/" style="color:#60a5fa;">الرئيسية</a>
    </div>
</div>
"""

@app.route('/')
def home():
    content = "<h3>مرحباً بك في منصتك</h3><a href='/register' style='color:white;'>إنشاء حساب</a><br><a href='/login' style='color:white;'>تسجيل الدخول</a>"
    return render_template_string(layout, content=content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    content = "<h2>تسجيل حساب</h2><form method='POST'><input name='username' placeholder='اسم المستخدم' required><br><input name='password' type='password' placeholder='كلمة المرور' required><br><button type='submit'>إنشاء</button></form>"
    return render_template_string(layout, content=content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        return "تم الدخول بنجاح!" if user else "خطأ في البيانات"
    content = "<h2>تسجيل الدخول</h2><form method='POST'><input name='username' placeholder='اسم المستخدم' required><br><input name='password' type='password' placeholder='كلمة المرور' required><br><button type='submit'>دخول</button></form>"
    return render_template_string(layout, content=content)

if __name__ == '__main__':
    app.run()
