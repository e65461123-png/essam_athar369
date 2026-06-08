def get_btc_price():
    try:
        # إضافة Headers للتعريف بأن الطلب يأتي من متصفح، مما يمنع الحظر
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=15, headers=headers)
        data = response.json()
        return f"{float(data['price']):,.0f}"
    except Exception as e:
        # يمكننا الآن رؤية سبب الخطأ في الـ Logs الخاصة بـ Render
        print(f"Connection Error: {e}")
        return "جاري التحديث..."
