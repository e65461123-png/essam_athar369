from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_btc_price():
    try:
        # رابط بديل ومباشر
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=10)
        data = response.json()
        price = float(data['price'])
        return f"{price:,.0f}" # يظهر الرقم بدون كسور
    except Exception as e:
        print(f"Error: {e}") # هذا سيظهر لك الخطأ الحقيقي في الـ Logs
        return "سيرفر مؤقت"

@app.route('/')
def home():
    price = get_btc_price()
    return render_template('index.html', btc_price=price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
