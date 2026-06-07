from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

# هذا هو المسار الجديد الذي سيجلب البيانات لـ JavaScript
@app.route('/api/prices')
def get_prices():
    # هنا ستضع لاحقاً كود الاتصال بالـ API الحقيقي
    # حالياً هذه أرقام تجريبية لترى التحديث في الصفحة
    return jsonify({
        "btc": "68400.00", 
        "gold": "2345.50"
    })

if __name__ == '__main__':
    app.run(debug=True)
