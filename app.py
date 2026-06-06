from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atheer_369.db'
db = SQLAlchemy(app)

# 1. نظام الحسابات (الخزنة المركزية)
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=1000.0)

# 2. نظام التدقيق (Audit Log - قلب الـ 61 نقطة)
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

# 3. محرك العمليات المالية (FinTech Engine)
@app.route('/api/invest', methods=['POST'])
def invest():
    account = Account.query.first()
    amount = 50.0
    account.balance += amount
    
    # تسجيل العملية في سجل التدقيق (إلزامي)
    log = AuditLog(action="INVESTMENT_BONUS", amount=amount)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({"new_balance": account.balance, "status": "SECURED"})

@app.route('/api/balance', methods=['GET'])
def get_balance():
    account = Account.query.first()
    return jsonify({"balance": account.balance})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
