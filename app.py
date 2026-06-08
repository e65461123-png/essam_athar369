from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()

def get_btc_price():
    try:
        # استخدام رابط Coingecko لأنه أكثر استقراراً
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=5)
        return response.json()['bitcoin']['usd']
    except:
        return "جاري الاتصال..."

layout = """
<div style="text-align:center; padding-top:50px; font-family:Tahoma; background:#0f172a; color:white; min-height:100vh;">
    <h1>AETHER 369</h1>
    <div style="width:300px; margin:auto; background:#1e293b; padding:20px; border-radius:15px;">
        {{ content | safe }}
    </div>
</div>
"""

@app.route('/')
def home():
    price = get_btc_price()
    content = f"<h2>سعر البيتكوين: {price} $</h2><a href='/register' style='color:white;'>إنشاء حساب</a> | <a href='/login' style='color:white;'>دخول</a>"
    return render_template_string(layout, content=content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        user = User(username=request.form['username'], password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    content = "<h2>تسجيل حساب</h2><form method='POST'><input name='username' placeholder='اسم المستخدم' required><br><input name='password' type='password' placeholder='كلمة المرور' required><br><button type='submit'>إنشاء</button></form>"
    return render_template_string(layout, content=content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            return "تم الدخول بأمان!"
        return "خطأ في البيانات"
    content = "<h2>تسجيل الدخول</h2><form method='POST'><input name='username' placeholder='اسم المستخدم' required><br><input name='password' type='password' placeholder='كلمة المرور' required><br><button type='submit'>دخول</button></form>"
    return render_template_string(layout, content=content)

if __name__ == '__main__':
    app.run()
