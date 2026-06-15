import requests
import time

# بياناتك الشخصية
BOT_TOKEN = "ضع_التوكن_هنا"
CHAT_ID = "-1004380080634"

# قائمة المنتجات (أضف هنا أي عدد تريده من المنتجات)
# ملاحظة: ضع رابط الأفلييت الخاص بك بدلاً من الروابط العادية
products_list = [
    {"name": "هاتف OnePlus", "url": "رابط_المنتج_1_الخاص_بك"},
    {"name": "ساعة ذكية", "url": "رابط_المنتج_2_الخاص_بك"},
    {"name": "سماعات بلوتوث", "url": "رابط_المنتج_3_الخاص_بك"}
]

def send_message(name, url):
    message = (
        f"🔥 **عرض مميز من أمازون**\n\n"
        f"📱 المنتج: {name}\n"
        f"🔗 اطلب الآن من الرابط التالي:\n{url}\n\n"
        f"⚠️ الأسعار تتغير بسرعة، تأكد من السعر قبل الشراء!"
    )
    url_api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url_api, params={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def monitor():
    while True:
        for item in products_list:
            try:
                # هنا سيقوم البوت بإرسال كل منتج في القائمة لقناتك
                send_message(item['name'], item['url'])
                time.sleep(10) # انتظار 10 ثوانٍ بين كل منتج والآخر
            except Exception as e:
                print(f"حدث خطأ: {e}")
        
        # البوت سينتظر ساعة كاملة قبل إعادة الدورة
        time.sleep(3600)

if __name__ == "__main__":
    monitor()
