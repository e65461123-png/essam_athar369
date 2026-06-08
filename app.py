from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_btc_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=5)
        return response.json()['bitcoin']['usd']
    except:
        return "N/A"

@app.route('/')
def home():
    price = get_btc_price()
    return render_template('index.html', btc_price=price)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
