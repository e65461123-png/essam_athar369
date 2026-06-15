import requests
import time

BOT_TOKEN = "ضع_التوكن_الخاص_بك"
CHAT_ID = "-1004380080634"

# قائمة المنتجات (أضف هنا أي منتج تريد مراقبته)
products_list = [
    {"name": "هاتف OnePlus Nord", "url": "رابط_المنتج_1"},
    {"name": "ساعة ذكية هواوي", "url": "رابط_المنتج_2"}
]

def check_and_post():
    for item in products_list:
        # هنا يتم وضع رابط الأفلييت الخاص بك
        affiliate_url = "https://amzn.to/رابطك_الخاص"
        
        # رسالة جذابة للمشتركين
        message = (
            f"🔥 **عرض حصري لا يفوت!**\n\n"
            f"📱 المنتج: {item['name']}\n"
            f"💰 السعر: انخفض الآن!\n\n"
            f"👇 **احصل عليه من هنا قبل نفاد الكمية:**\n"
            f"{affiliate_url}\n\n"
            f"🔔 *ملاحظة: الأسعار تتغير بسرعة، تأكد من السعر عند الدخول!*"
        )
        
        # إرسال الرسالة للقناة
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, params={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        
        # تأخير بسيط لحماية القناة من التنبيهات المتكررة
        time.sleep(10)

# حلقة المراقبة
while True:
    check_and_post()
    time.sleep(3600) # البوت سيفحص القائمة كل ساعة
