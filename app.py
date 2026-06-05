from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY, balance REAL)')
    c.execute('INSERT OR IGNORE INTO vault (id, balance) VALUES (1, 0.0)')
    conn.commit()
    c.execute('SELECT balance FROM vault WHERE id = 1')
    result = c.fetchone()
    current_balance = result[0] if result else 0
    conn.close()
    return render_template('essam.html', balance=current_balance, ticker="سوق ATHEER 369 نشط")

@app.route('/activate-flow', methods=['POST'])
def activate_flow():
    # حساب المبلغ بعد خصم 10%
    final_amount = 100 * 0.90
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('UPDATE vault SET balance = balance + ? WHERE id = 1', (final_amount,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "تم الإيداع"})

if __name__ == '__main__':
    app.run(debug=True)
