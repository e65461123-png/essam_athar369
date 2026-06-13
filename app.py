import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# استخدام متغير البيئة (قم بإضافته في Render تحت اسم OPENAI_API_KEY)
openai.api_key = os.environ.get("OPENAI_API_KEY")

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Viral AI</title>
    <style>
        body { margin:0; font-family:Arial,sans-serif; background:linear-gradient(135deg,#0f172a,#1e293b); min-height:100vh; display:flex; justify-content:center; align-items:center; padding: 20px; }
        .card { width:100%; max-width:500px; background:white; padding:30px; border-radius:20px; box-shadow:0 10px 30px rgba(0,0,0,.3); text-align:center; }
        h1 { color:#2563eb; }
        input { width:100%; padding:15px; margin-top:15px; border:1px solid #ddd; border-radius:10px; box-sizing: border-box; }
        button { width:100%; padding:15px; margin-top:15px; border:none; border-radius:10px; background:#2563eb; color:white; font-size:18px; cursor:pointer; }
        #result { margin-top:20px; text-align:right; padding:15px; background:#f3f4f6; border-radius:10px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Viral AI</h1>
        <p>أدخل رابط الفيديو لتحليله بالذكاء الاصطناعي</p>
        <input type="text" id="url" placeholder="ضع رابط الفيديو هنا">
        <button onclick="analyze()">تحليل الفيديو</button>
        <div id="result"></div>
    </div>
    <script>
        async function analyze(){
            let url = document.getElementById("url").value;
            let resDiv = document.getElementById("result");
            resDiv.innerText = "⏳ جاري التحليل... يرجى الانتظار";
            try {
                const response = await fetch("/analyze", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({url: url})
                });
                const data = await response.json();
                resDiv.innerText = data.analysis;
            } catch(e) {
                resDiv.innerText = "❌ حدث خطأ أثناء الاتصال بالخادم";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_CONTENT

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({"analysis": "يرجى إدخال رابط فيديو صالح."})
    
    try:
        # الاتصال الحقيقي بـ OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"حلل هذا الفيديو واستخرج عنواناً جذاباً وهاشتاجات فيروسية: {video_url}"}]
        )
        return jsonify({"analysis": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"analysis": f"خطأ في التحليل: {str(e)}"})

if __name__ == '__main__':
    app.run()
