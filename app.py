from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY, balance REAL)')
    c.execute('INSERT OR IGNORE INTO vault (id, balance) VALUES (1, 0.0)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT balance FROM vault WHERE id = 1')
    current_balance = c.fetchone()[0]
    conn.close()
    ticker = f"GOLD: ${2300.89 + random.random():.2f} | BTC: ${68016 + random.randint(1,100)}"
    return render_template('Essam.html', balance=current_balance, ticker=ticker)

@app.route('/activate-flow', methods=['POST'])
def activate_flow():
    # هنا يتم تنفيذ منطق التفعيل
    return jsonify({"status": "success", "message": "تم تفعيل بوابة التدفق المالي بنجاح"})

if __name__ == '__main__':
    app.run(debug=True)
