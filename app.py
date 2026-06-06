from flask import Flask, jsonify, render_template_string, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atheer_369.db'
db = SQLAlchemy(app)

# 1. هيكل قاعدة البيانات
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=1000.0)
    gold = db.Column(db.Float, default=0.0)

# 2. واجهة المستخدم (الفرونت إند المدمج)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ATHEER 369 | منصة التداول</title>
    <style>
        body { background: #0b0e11; color: #eaecef; font-family: sans-serif; margin: 0; padding: 20px; }
        .nav { background: #1e2329; padding: 15px; border-radius: 10px; display: flex; justify-content: space-between; }
        .market { background: #1e2329; padding: 20px; margin-top: 20px; border-radius: 10px; }
        button { padding: 12px 25px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold; margin: 5px; }
        .buy { background: #0ecb81; color: white; }
        .sell { background: #f6465d; color: white; }
    </style>
</head>
<body>
    <div class="nav">
        <b>ATHEER 369</b>
        <div>الرصيد: <span id="bal">{{ user.balance }}</span> $ | الذهب: <span id="gold">{{ user.gold }}</span></div>
    </div>
    <div class="market">
        <h3>السوق المباشر</h3>
        <button class="buy" onclick="trade('BUY')">شراء (50$)</button>
        <button class="sell" onclick="trade('SELL')">بيع (50$)</button>
    </div>
    <script>
        async function trade(type) {
            const res = await fetch('/api/trade', {
                method: 'POST', 
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: type})
            });
            const data = await res.json();
            document.getElementById('bal').innerText = data.balance;
            document.getElementById('gold').innerText = data.gold;
        }
    </script>
</body>
</html>
"""

# إعداد قاعدة البيانات عند التشغيل
with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(balance=1000.0, gold=0.0))
        db.session.commit()

@app.route('/')
def home():
    user = User.query.first()
    return render_template_string(HTML_TEMPLATE, user=user)

@app.route('/api/trade', methods=['POST'])
def trade():
    data = request.json
    user = User.query.first()
    if data['type'] == 'BUY' and user.balance >= 50:
        user.balance -= 50
        user.gold += 1
    elif data['type'] == 'SELL' and user.gold >= 1:
        user.balance += 50
        user.gold -= 1
    db.session.commit()
    return jsonify({"balance": user.balance, "gold": user.gold})

if __name__ == '__main__':
    app.run(debug=True)
