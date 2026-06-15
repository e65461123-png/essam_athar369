import requests
import time

# 1. ضع الـ TOKEN الخاص بالبوت هنا
BOT_TOKEN = "ضع_توكن_البوت_الخاص_بك_هنا"

# 2. هذا هو التعديل الجديد (رقم القناة الذي استخرجناه)
CHAT_ID = "-1004380080634"

def send_to_channel(price, product_name):
    # رسالة احترافية لجذب المتابعين
    message = f"🔥 **تحديث سعر أمازون:**\n\n📱 المنتج: {product_name}\n💰 السعر الحالي: {price} جنيه\n\n🔗 اشترِ الآن من الرابط التالي:\n[ضع_رابط_الأفلييت_الخاص_بك_هنا]"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, params=params)

# ... (باقي الكود الخاص بك الذي يجلب السعر من أمازون)
