from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

@app.route('/')
def index():
    return "<h1>مرحباً بك في المحفظة الرقمية</h1>"

@app.route('/initdb')
def initdb():
    db.create_all()
    return "تم إنشاء الجداول بنجاح!"

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    data = request.json
    username = data.get('username')
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "المستخدم موجود بالفعل!"}), 400
    new_user = User(username=username, balance=100.0)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": f"تم إنشاء محفظة لـ {username} برصيد 100!"}), 201

# --- الإضافة الجديدة ---
@app.route('/balance/<username>')
def get_balance(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return f"<h1>مرحباً {user.username}</h1><p>رصيدك الحالي هو: {user.balance} دولار</p>"
    return "<h1>المستخدم غير موجود</h1>"

if __name__ == '__main__':
    app.run()
