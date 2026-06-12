import os
from flask import Flask, request, jsonify, render_template_string
import yt_dlp

app = Flask(__name__)

# صفحة الواجهة الرئيسية
HTML_CONTENT = """
<html><body><h1>الموقع يعمل بنجاح!</h1>
<p>أدخل رابط الفيديو في API/analyze</p>
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_CONTENT)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    video_url = data.get('url', '')
    
    # استخراج معلومات الفيديو فقط (سريع ولا يستهلك ذاكرة)
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'فيديو رائع')
    except Exception:
        title = "خطأ في جلب بيانات الفيديو"

    return jsonify({
        "success": True,
        "title": title,
        "message": "تمت العملية بنجاح دون تحميل ملفات ثقيلة!"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
