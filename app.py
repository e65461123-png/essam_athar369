from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_btc_price():
    try:
        # جلب السعر من Binance مباشرة
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=10)
        data = response.json()
        price = float(data['price'])
        return f"{price:,.2f}" # تنسيق الرقم ليظهر بشكل جميل
    except:
        return "N/A"

@app.route('/')
def home():
    price = get_btc_price()
    return render_template('index.html', btc_price=price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
