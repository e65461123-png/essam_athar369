import os
from flask import Flask, request, jsonify, render_template_string
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

app = Flask(__name__)

# [HTML_CONTENT كما هي لا تغيرها، فقط ضعها في بداية الملف]
HTML_CONTENT = """...""" # (ضع نفس كود الـ HTML القديم هنا)

@app.route("/")
def home():
    return render_template_string(HTML_CONTENT)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    video_url = data.get('url', '')

    # 1. تحميل الفيديو
    ydl_opts = {'format': 'best', 'outtmpl': 'input_video.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # 2. هنا نضع منطق Gemini (سيعطيك التوقيتات)
    # سنفترض أن Gemini اختار القص من الثانية 5 إلى 35
    start_time = 5
    end_time = 35

    # 3. قص الفيديو باستخدام MoviePy
    with VideoFileClip("input_video.mp4") as video:
        new = video.subclip(start_time, end_time)
        new.write_videofile("output_viral.mp4", codec="libx264")

    return jsonify({
        "success": True,
        "time_frame": f"{start_time} - {end_time}",
        "title": "تم قص مقطع فيروسي بنجاح!",
        "tags": "#تجربة #نجاح #Viral"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
