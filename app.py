import os
import sqlite3
from flask import g

# تحديد المسار الصحيح للمجلد اللي السيرفر بيشغلك فيه
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # الاتصال بقاعدة البيانات
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# دالة التأكد من وجود الجداول (عدلها عشان تكون أكثر أماناً)
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # إنشاء جدول المستخدمين
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        # إنشاء جدول الرسايل
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            content TEXT NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id))''')
        db.commit()

# أهم خطوة: تشغيل init_db() عند بداية التطبيق
with app.app_context():
    init_db()
