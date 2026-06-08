from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_btc_price():
    try:
        # استخدام مهلة زمنية كافية وتجاهل التحقق من SSL لضمان استقرار الاتصال
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=20, verify=False)
        data = response.json()
        
        # التأكد من أن البيانات تحتوي على السعر
        if 'price' in data:
            price = float(data['price'])
            return f"{price:,.0f}"
        else:
            return "بيانات غير متوفرة"
    except Exception as e:
        # إذا حدث أي خطأ، سيرجع القيمة التالية
        return "خطأ اتصال"

@app.route('/')
def home():
    price = get_btc_price()
    return render_template('index.html', btc_price=price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
