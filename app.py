from flask import Flask, render_template_string, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# إعداد قاعدة البيانات في ملف محلي
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# تعريف جدول المستخدم
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), default="عصام")
    balance = db.Column(db.Float, default=1250.00)

# إنشاء القاعدة تلقائياً
with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(username="عصام", balance=1250.00))
        db.session.commit()

# الواجهة التي أرسلتها (تم دمجها)
HOME_HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<title>Wallet Dashboard</title>
<style>
body{margin:0; font-family: 'Segoe UI', sans-serif; background: radial-gradient(circle at top, #0f172a, #020617); color:white; display:flex; justify-content:center; align-items:center; height:100vh;}
.card{width:380px; padding:25px; border-radius:20px; background: rgba(255,255,255,0.08); backdrop-filter: blur(12px); box-shadow: 0 0 30px rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.1); text-align:center;}
h2{color:#38bdf8; margin-bottom:5px;}
.balance{font-size:24px; color:#22c55e; margin:15px 0;}
input{width:90%; padding:12px; margin-top:10px; border:none; border-radius:10px; outline:none; font-size:15px;}
.btn{width:45%; padding:12px; margin-top:10px; border:none; border-radius:10px; font-weight:bold; cursor:pointer; transition:0.3s;}
.deposit{background:#22c55e; color:white;}
.withdraw{background:#ef4444; color:white;}
.btn:hover{transform: scale(1.05);}
</style>
</head>
<body>
<div class="card">
    <h2>مرحباً {{ user }}</h2>
    <div class="balance">💰 USD {{ "%.2f"|format(balance) }}</div>
    <form method="POST" action="/update_balance">
        <input name="amount" type="number" step="0.01" placeholder="أدخل المبلغ" required>
        <div>
            <button class="btn deposit" name="action" value="deposit">إيداع</button>
            <button class="btn withdraw" name="action" value="withdraw">سحب</button>
        </div>
    </form>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    user = User.query.first()
    return render_template_string(HOME_HTML, user=user.username, balance=user.balance)

@app.route('/update_balance', methods=['POST'])
def update_balance():
    amount = float(request.form.get('amount', 0))
    action = request.form.get('action')
    user = User.query.first()
    
    if action == 'deposit':
        user.balance += amount
    elif action == 'withdraw' and user.balance >= amount:
        user.balance -= amount
        
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run()
