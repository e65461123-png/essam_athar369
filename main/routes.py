from flask import Blueprint, render_template, request, jsonify
import sqlite3
from app import create_app

main_bp = Blueprint('main', __name__)

def get_db():
    """الاتصال بقاعدة البيانات"""
    app = create_app()
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """تهيئة قاعدة البيانات"""
    app = create_app()
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS family (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            relationship TEXT,
            phone TEXT,
            address TEXT
        )
    ''')
    
    # بيانات نموذجية
    cursor.execute("SELECT COUNT(*) FROM family")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ('أحمد محمد', 30, 'أب', '0501234567', 'الرياض'),
            ('سارة أحمد', 28, 'أم', '0501234568', 'الرياض'),
            ('علي أحمد', 10, 'ابن', '0501234569', 'الرياض'),
        ]
        cursor.executemany(
            "INSERT INTO family (name, age, relationship, phone, address) VALUES (?, ?, ?, ?, ?)",
            sample_data
        )
    
    conn.commit()
    conn.close()

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/report', methods=['GET', 'POST'])
def report():
    result = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            conn = get_db()
            data = conn.execute("SELECT * FROM family WHERE name LIKE ?", (f'%{name}%',)).fetchall()
            conn.close()
            result = data
    return render_template('report.html', result=result)

@main_bp.route('/api/search/<name>')
def api_search(name):
    conn = get_db()
    data = conn.execute("SELECT * FROM family WHERE name LIKE ?", (f'%{name}%',)).fetchall()
    conn.close()
    return jsonify({
        "status": "success",
        "count": len(data),
        "data": [dict(row) for row in data]
    })
