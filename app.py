from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# تعريف جدول المستخدم
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

# مسار إنشاء الجدول (للمرة الأولى)
@app.route('/initdb')
def initdb():
    db.create_all()
    return "تم إنشاء جداول قاعدة البيانات بنجاح!"

# مسار إنشاء المحفظة
@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    data = request.json
    username = data.get('username')
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "المستخدم موجود بالفعل!"}), 400
    new_user = User(username=username, balance=0.0)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": f"تم إنشاء محفظة للمستخدم {username} بنجاح!"}), 201

if __name__ == '__main__':
    app.run()
