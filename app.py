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
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=5)
        return response.json()['bitcoin']['usd']
    except:
        return "N/A"

# واجهة بسيطة ومستقرة (بدون تعقيد في الـ Template)
def get_layout(content):
    return f"""
    <div style="text-align:center; padding:50px; background:#0f172a; color:white; font-family:Arial;">
        <div style="background:#1e293b; padding:30px; border-radius:20px; width:300px; margin:auto;">
            <h1>AETHER 369</h1>
            {content}
        </div>
    </div>
    """

@app.route('/')
def home():
    price = get_btc_price()
    content = f"<h2>BTC: {price} $</h2><br><a href='/register' style='color:white;'>إنشاء</a> | <a href='/login' style='color:white;'>دخول</a>"
    return get_layout(content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        user = User(username=request.form['username'], password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    content = "<h2>تسجيل</h2><form method='POST'><input name='username' placeholder='الاسم'><br><input name='password' type='password' placeholder='الباسورد'><br><button type='submit'>إنشاء</button></form>"
    return get_layout(content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            return "تم الدخول!"
        return "خطأ!"
    content = "<h2>دخول</h2><form method='POST'><input name='username' placeholder='الاسم'><br><input name='password' type='password' placeholder='الباسورد'><br><button type='submit'>دخول</button></form>"
    return get_layout(content)

if __name__ == '__main__':
    app.run()
