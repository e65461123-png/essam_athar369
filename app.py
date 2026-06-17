import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g

app = Flask(__name__)
app.secret_key = 'super-secret-key' # غيرها لشيء سري في الحقيقة

# المسار الصحيح للداتابيز على أي سيرفر
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)''')
        db.commit()

# تشغيل التهيئة مرة واحدة عند بدء التطبيق
init_db()

@app.route('/')
def home():
    return "مرحباً بك في التطبيق الذكي! اذهب لـ /login للدخول."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # منطق تسجيل الدخول هنا
        return "تمت محاولة الدخول!"
    return "صفحة تسجيل الدخول"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
