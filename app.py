from flask import Flask, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atheer_369.db'
db = SQLAlchemy(app)

# 1. نظام الحسابات (الخزنة المركزية)
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=1000.0)

# 2. سجل التدقيق الشامل (بند التوثيق المالي)
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    if not Account.query.first():
        db.session.add(Account(balance=1000.0))
        db.session.commit()

# واجهة المستخدم الاحترافية (تصميم الـ 61 بند للنمو)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ATHEER 369 - منصة التداول العالمية</title>
    <style>
        body { background: #0b0e11; color: #eaecef; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 20px; }
        .dashboard { background: #1e2329; padding: 30px; border-radius: 15px; display: inline-block; width: 90%; max-width: 400px; border: 1px solid #363c4e; }
        .balance { font-size: 2em; color: #f3ba2f; margin: 20px 0; }
        button { background: #f3ba2f; border: none; padding: 15px 30px; border-radius: 5px; font-weight: bold; cursor: pointer; color: #000; width: 100%; font-size: 1.1em; }
        button:hover { background: #e0ab2a; }
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>ATHEER 369</h1>
        <p>رصيدك المحمي</p>
        <div class="balance" id="balance">{{ balance }} $</div>
        <button onclick="invest()">استثمار وتوثيق (Audit)</button>
    </div>
    <script>
        async function invest() {
            const res = await fetch('/api/invest', {method: 'POST'});
            const data = await res.json();
            document.getElementById('balance').innerText = data.new_balance;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    account = Account.query.first()
    return render_template_string(HTML_TEMPLATE, balance=account.balance)

@app.route('/api/invest', methods=['POST'])
def invest():
    account = Account.query.first()
    amount = 50.0
    account.balance += amount
    
    # تسجيل العملية في سجل التدقيق (جوهر الـ 61 بند)
    log = AuditLog(action="USER_INVESTMENT", amount=amount)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({"new_balance": account.balance})

if __name__ == '__main__':
    app.run()
