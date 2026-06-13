import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
# تأكد من إضافة مفتاحك في إعدادات Render كمتغير بيئة باسم OPENAI_API_KEY
openai.api_key = os.environ.get("OPENAI_API_KEY")

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Viral AI</title>
    <style>
        body{font-family:Arial,sans-serif;background:#0f172a;color:white;text-align:center;padding:50px;}
        .card{background:white;color:black;padding:20px;border-radius:15px;max-width:400px;margin:auto;}
        input, button{width:100%;padding:10px;margin-top:10px;border-radius:5px;}
        button{background:#2563eb;color:white;border:none;cursor:pointer;}
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Viral AI</h1>
        <input type="text" id="url" placeholder="ضع رابط الفيديو هنا">
        <button onclick="analyze()">تحليل الفيديو</button>
        <div id="result" style="margin-top:20px;"></div>
    </div>
    <script>
        async function analyze(){
            let url = document.getElementById("url").value;
            document.getElementById("result").innerText = "⏳ جاري التحليل بواسطة الذكاء الاصطناعي...";
            let res = await fetch("/analyze", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({url: url})
            });
            let data = await res.json();
            document.getElementById("result").innerText = data.analysis;
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
    url = data.get('url')
    if not url: return jsonify({"analysis": "الرجاء إدخال رابط"}), 400
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"حلل هذا الفيديو واستخرج عنواناً جذاباً وهاشتاجات: {url}"}]
        )
        return jsonify({"analysis": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"analysis": "حدث خطأ: " + str(e)})

if __name__ == '__main__':
    app.run()
