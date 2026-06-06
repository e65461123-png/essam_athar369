from flask import Flask, render_template
import requests

app = Flask(__name__)

# دالة لجلب سعر البيتكوين الحي من بورصة بينانس مباشرة
def get_live_btc_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=5)
        data = response.json()
        # تقريب السعر لرقمين عشريين وفصل الآلاف بفاصلة لشكل احترافي
        price = float(data['price'])
        return f"{price:,.2f}"
    except:
        # سعر احتياطي لو النت علق في السيرفر مؤقتاً
        return "68,230.00"

# لوحة تحكم المستخدم العادي (العميل) - المسار الرئيسي للموقع
@app.route('/')
@app.route('/dashboard')
def user_dashboard():
    btc_live = get_live_btc_price()
    
    user_data = {
        'username': 'عصام الكومي',
        'wallet_balance': '1,250.00',
        'btc_price': btc_live,      # السعر الحي من بينانس هنا
        'gold_price': '2,340.00'     # سعر الذهب ثابت مؤقتاً للمرحلة الجاية
    }
    return render_template('user_dashboard.html', data=user_data)

# لوحة تحكم الأدمن (المسؤول)
@app.route('/admin/dashboard')
def admin_dashboard():
    admin_data = {
        'username': 'admin',
        'balance': '369.0'
    }
    return render_template('dashboard.html', data=admin_data)

if __name__ == '__main__':
    app.run(debug=True)
