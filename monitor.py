import requests
import time

BOT_TOKEN = "ضع_التوكن_الخاص_بك"
CHAT_ID = "-1004380080634"

# هنا نضع قائمة المنتجات (أضف أي عدد تريده)
products_list = [
    {"name": "هاتف OnePlus", "url": "رابط_المنتج_1"},
    {"name": "ساعة ذكية", "url": "رابط_المنتج_2"},
    {"name": "سماعات بلوتوث", "url": "رابط_المنتج_3"}
]

def check_and_post():
    for item in products_list:
        # هنا ستضع الكود الذي يجلب السعر من الرابط
        # price = get_price_from_url(item['url']) 
        
        # لنفترض أنك حصلت على السعر
        price = "تم جلب السعر" 
        
        message = f"🔥 عرض جديد!\n📱 المنتج: {item['name']}\n💰 السعر: {price}\n🔗 اشترِ الآن: [رابط_الأفلييت_الخاص_بك]"
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, params={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        
        # انتظار بسيط بين كل رسالة والأخرى لتجنب الحظر من تليجرام
        time.sleep(5)

# تشغيل المراقبة في حلقة مستمرة
while True:
    check_and_post()
    time.sleep(3600) # فحص كل ساعة
