from flask import Flask, jsonify, render_template_string, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atheer_369.db'
db = SQLAlchemy(app)

# قاعدة بيانات متكاملة: مستخدم، محفظة، سجل تدقيق
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=1000.0)
    gold = db.Column(db.Float, default=0.0)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(balance=1000.0, gold=0.0))
        db.session.commit()

# واجهة شاملة (الرئيسية + السوق + المحفظة)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <style>
        body { background: #0b0e11; color: white; font-family: sans-serif; margin: 0; padding: 20px; }
        .nav { background: #1e2329; padding: 15px; border-radius: 10px; margin-bottom: 20px; display: flex; gap: 20px; }
        .card { background: #1e2329; padding: 20px; border-radius: 10px; margin-bottom: 10px; }
        button { padding: 10px 20px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="nav"> <b>ATHEER 369</b> | الرصيد: <span id="bal">{{ user.balance }}</span> $ | الذهب: <span id="gold">{{ user.gold }}</span> </div>
    <div class="card">
        <h3>السوق المباشر</h3>
        <p>شراء الذهب (سعر 50$): <button onclick="trade('BUY')">شراء</button></p>
        <p>بيع الذهب (سعر 50$): <button onclick="trade('SELL')">بيع</button></p>
    </div>
    <script>
        async function trade(type) {
            const res = await fetch('/api/trade', {method: 'POST', body: JSON.stringify({type: type}), headers: {'Content-Type': 'application/json'}});
            const data = await res.json();
            document.getElementById('bal').innerText = data.balance;
            document.getElementById('gold').innerText = data.gold;
        }
    </script>
</body>
</html>
"""

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
    app.run()
