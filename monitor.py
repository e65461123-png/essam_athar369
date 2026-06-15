import requests
import time

# 1. ضع هنا التوكن الخاص ببوتك (احصل عليه من BotFather)
BOT_TOKEN = "ضع_التوكن_الخاص_بك_هنا"

# 2. هذا هو رقم القناة الخاص بك (لا تغيره)
CHAT_ID = "-1004380080634"

def send_to_channel(price, product_name):
    # 3. ضع هنا رابط الأفلييت الخاص بك من أمازون
    affiliate_link = "ضع_رابط_الأفلييت_الخاص_بك_هنا"
    
    message = f"🔥 **تحديث سعر أمازون:**\n\n📱 المنتج: {product_name}\n💰 السعر الحالي: {price} جنيه\n\n🔗 اشترِ الآن من الرابط التالي:\n{affiliate_link}"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, params=params)

# ... (هنا يتم وضع كود جلب السعر من أمازون)
