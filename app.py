from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atheer_369.db'
db = SQLAlchemy(app)

# --- هيكلية النظام (الدستور: 61 نقطة) ---

# 1. الخزنة المركزية
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=1000.0)

# 2. سجل التدقيق (Audit Log) - لضمان الشفافية ومحاسبة كل قرش
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

# --- واجهات النظام (Endpoints) ---

# المسار الرئيسي (حل مشكلة Not Found)
@app.route('/')
def home():
    return "ATHEER 369 System Online - النظام المالي يعمل وفق دستور الـ 61 نقطة."

# محرك الاستثمار بنسبة 10%
@app.route('/api/invest', methods=['POST'])
def invest():
    account = Account.query.first()
    amount = 50.0  # قيمة افتراضية للاستثمار
    account.balance += amount
    
    # تسجيل العملية في سجل التدقيق (بند إلزامي)
    log = AuditLog(action="INVESTMENT_SUCCESS", amount=amount)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({"new_balance": account.balance, "status": "SECURED_AND_AUDITED"})

# استعلام الرصيد
@app.route('/api/balance', methods=['GET'])
def get_balance():
    account = Account.query.first()
    return jsonify({"balance": account.balance, "currency": "USD"})

if __name__ == '__main__':
    app.run()
