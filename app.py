from flask import Flask, render_template
import requests

app = Flask(__name__)

# دالة جلب سعر البيتكوين الحي مباشرة من بينانس
def get_btc():
    try:
        return f"{float(requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=3).json()['price']):,.2f}"
    except:
        return "68,230.00"

# 1. لوحة تحكم المستخدم العادي (العميل) - المسار الرئيسي للموقع
@app.route('/')
@app.route('/dashboard')
def user_dashboard():
    user_data = {
        'username': 'عصام الكومي',
        'wallet_balance': '1,250.00',
        'btc_price': get_btc(),  # السعر الحي هيسمع هنا فوراً
        'gold_price': '2,340.00'
    }
    # متظبطة هنا عشان تقرأ ملفك اللي اسمه dashboard.html اللي في المجلد فوراً
    return render_template('dashboard.html', data=user_data)

# 2. لوحة تحكم الأدمن (المسؤول)
@app.route('/admin/dashboard')
def admin_dashboard():
    admin_data = {
        'username': 'admin',
        'balance': '369.0'
    }
    return render_template('dashboard.html', data=admin_data)

if __name__ == '__main__':
    app.run(debug=True)
