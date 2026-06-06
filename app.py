from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# الاتصال بقاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# تعريف جدول المستخدمين
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

# الصفحة الرئيسية (بدل صفحة الاختبار)
@app.route('/')
def index():
    return "<h1>مرحباً بك في المحفظة الرقمية</h1>"

# إنشاء الجداول (قم بزيارة الرابط /initdb مرة واحدة)
@app.route('/initdb')
def initdb():
    db.create_all()
    return "تم إنشاء الجداول بنجاح!"

# إنشاء محفظة لمستخدم جديد
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

if __name__ == '__main__':
    app.run()
