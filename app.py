import logging
from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# استخدم قاعدة بيانات بدلاً من القائمة (مثال SQLite)
import sqlite3
def init_db():
    conn = sqlite3.connect('radar.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  data TEXT)''')
    conn.commit()
    conn.close()
init_db()

@app.route('/report', methods=['POST'])
def report():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        # تحقق من وجود حقول أساسية (مثال)
        if 'source' not in data or 'value' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        # تخزين في قاعدة البيانات
        conn = sqlite3.connect('radar.db')
        c = conn.cursor()
        c.execute("INSERT INTO logs (timestamp, data) VALUES (?, ?)",
                  (datetime.utcnow().isoformat(), str(data)))
        conn.commit()
        conn.close()
        logging.info(f"Received: {data}")
        return jsonify({"status": "received"}), 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/logs')
def get_logs():
    # أضف مصادقة بسيطة باستخدام مفتاح في رأس الطلب
    api_key = request.headers.get('X-API-Key')
    if api_key != os.environ.get('ADMIN_API_KEY', 'secret'):
        return jsonify({"error": "Unauthorized"}), 401
    conn = sqlite3.connect('radar.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, data FROM logs ORDER BY id DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"timestamp": r[0], "data": r[1]} for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
