from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 🔐 مفتاح الجلسات
app.config['SECRET_KEY'] = 'mysecretkey123'

# 📦 قاعدة البيانات SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 👤 جدول المستخدمين
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# 🏠 الصفحة الرئيسية
@app.route('/')
def home():
    if 'user' in session:
        return f"👋 مرحباً {session['user']} - <a href='/logout'>Logout</a>"
    return "🏠 Home - <a href='/login'>Login</a> | <a href='/register'>Register</a>"


# 🆕 تسجيل حساب
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return "❌ المستخدم موجود بالفعل"

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return "✅ تم إنشاء الحساب بنجاح"

    return '''
    <form method="post">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Register</button>
    </form>
    '''


# 🔐 تسجيل دخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            return redirect(url_for('home'))
        else:
            return "❌ بيانات غير صحيحة"

    return '''
    <form method="post">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    '''


# 🚪 تسجيل خروج
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


# ▶ تشغيل السيرفر
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
