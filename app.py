import openai # مكتبة للربط مع الذكاء الاصطناعي
from flask import Flask, request, jsonify

app = Flask(__name__)

# إعداد مفتاح الذكاء الاصطناعي (احصل عليه من OpenAI API)
openai.api_key = "YOUR_OPENAI_API_KEY"

def get_ai_analysis(video_url):
    # 1. هنا سنقوم بجلب محتوى الفيديو (Transcript) باستخدام yt-dlp
    # 2. إرسال النص إلى AI لاستخراج العناوين والهاشتاجات
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"حلل هذا الفيديو واستخرج عنواناً جذاباً وهاشتاجات: {video_url}"}]
    )
    return response.choices[0].message.content

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')
    
    # تنفيذ التحليل المؤتمت بالكامل
    result = get_ai_analysis(url)
    
    return jsonify({"analysis": result})
