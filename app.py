from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

# واجهة بسيطة جداً (بدل صفحة الاتصال)
@app.route('/')
def index():
    return "<h1>أهلاً بك في محفظتك الرقمية!</h1><p>استخدم /create_wallet لإنشاء محفظة.</p>"

@app.route('/initdb')
def initdb():
    db.create_all()
    return "تم إنشاء الجداول!"

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    data = request.json
    username = data.get('username')
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "المستخدم موجود!"}), 400
    new_user = User(username=username, balance=100.0) # هدية 100 رصيد
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": f"تم إنشاء محفظة لـ {username} برصيد 100!"}), 201

if __name__ == '__main__':
    app.run()
