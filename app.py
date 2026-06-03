from flask import Flask, render_template_string, request, redirect
import sqlite3
import random

app = Flask(__name__)

# إنشاء قاعدة البيانات والجدول عند التشغيل
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY, balance REAL)')
    c.execute('INSERT OR IGNORE INTO vault (id, balance) VALUES (1, 0.0)')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    if request.method == "POST":
        amount = float(request.form.get("amount", 0))
        c.execute('UPDATE vault SET balance = balance + ? WHERE id = 1', (amount * 0.10,))
        conn.commit()
    
    c.execute('SELECT balance FROM vault WHERE id = 1')
    current_balance = c.fetchone()[0]
    conn.close()
    
    ticker = f"GOLD: ${2300 + random.random():.2f} | BTC: ${68000 + random.randint(1,50)}"
    
    template = """
    <body style="background:#0a0a0a; color:#fff; font-family:monospace; text-align:center;">
        <div style="background:#111; padding:10px; color:#0f0; border-bottom:1px solid #333;">{{ ticker }}</div>
        <div style="border:1px solid #333; background:#111; width:350px; margin:50px auto; padding:20px; border-radius:10px;">
            <h1>ATHEER 369</h1>
            <h2>الرصيد: ${{ "%.2f"|format(balance) }}</h2>
            <form method="post">
                <input name="amount" type="number" step="0.01" style="background:#000; color:#fff; border:1px solid #444; padding:5px; width:80%;">
                <br><br><button type="submit" style="background:#00ff41; border:none; padding:10px 20px; font-weight:bold;">تنفيذ</button>
            </form>
        </div>
    </body>
    """
    return render_template_string(template, balance=current_balance, ticker=ticker)

if __name__ == "__main__": app.run()
