from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# وظيفة لحساب الرصيد بعد خصم عمولة 10%
def calculate_balance_with_fee(amount):
    fee = amount * 0.10
    return amount - fee

@app.route('/')
def home():
    # جلب الرصيد من قاعدة البيانات
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT balance FROM vault WHERE id = 1')
    result = c.fetchone()
    current_balance = result[0] if result else 0
    conn.close()
    return render_template('essam.html', balance=current_balance, ticker="سوق ATHEER 369 نشط")

@app.route('/activate-flow', methods=['POST'])
def activate_flow():
    # هنا نطبق منطق الـ 10%
    # سنفترض أن المستخدم أودع مبلغاً (مثلاً 100)
    deposit_amount = 100 
    final_amount = calculate_balance_with_fee(deposit_amount)
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('UPDATE vault SET balance = balance + ? WHERE id = 1', (final_amount,)
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": f"تمت إضافة {final_amount} (بعد خصم عمولة 10%)"})

if __name__ == '__main__':
    app.run(debug=True)
