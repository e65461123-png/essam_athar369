from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# هذا السطر يقرأ الرابط الذي وضعناه في إعدادات Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# --- ضع كود الجدول هنا ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<User {self.username}>'

# --- وضع كود إنشاء الجدول هنا ---
@app.route('/initdb')
def initdb():
    db.create_all()
    return "تم إنشاء جداول قاعدة البيانات بنجاح!"

# (وبقية كود الموقع الخاص بك هنا)
