from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_btc_price():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=15, headers=headers)
        data = response.json()
        return f"{float(data['price']):,.0f}"
    except Exception as e:
        print(f"Connection Error: {e}")
        return "جاري التحديث..."

@app.route('/')
def home():
    price = get_btc_price()
    return render_template('index.html', btc_price=price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
