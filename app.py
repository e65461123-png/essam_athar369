from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/prices')
def get_prices():
    try:
        # جلب سعر البيتكوين من CoinGecko
        btc_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd').json()
        btc_price = btc_response['bitcoin']['usd']

        # جلب سعر الذهب (كمثال، نستخدم سعر تقريبي نظراً لأن معظم API الذهب تتطلب مفتاح تسجيل)
        # يمكنك لاحقاً التسجيل في GoldAPI.io للحصول على مفتاح API خاص بك
        gold_price = "2345.50" 

        return jsonify({
            "btc": f"{btc_price:,.2f}",
            "gold": gold_price
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
