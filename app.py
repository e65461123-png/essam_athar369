from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'aether369_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aether360.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# تعريف الموديلات هنا لضمان وجودها
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

class Wallet(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    balance_usd = db.Column(db.Float, default=0.0)

with app.app_context():
    db.create_all()

# الـ Routes مباشرة هنا لتجنب أي مشاكل استيراد
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    wallet = Wallet.query.get(session['user_id'])
    return render_template('dashboard.html', user=user, wallet=wallet)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return "صفحة تسجيل الدخول"

if __name__ == '__main__':
    app.run()
