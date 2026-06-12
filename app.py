import os
from flask import Flask, request, jsonify, render_template_string
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

app = Flask(__name__)

# [ضع هنا كود الـ HTML الخاص بك كما هو]
HTML_CONTENT = """...""" 

@app.route("/")
def home():
    return render_template_string(HTML_CONTENT)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    video_url = data.get('url', '')
    
    # 1. إعدادات تحميل الفيديو
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'input_video.mp4',
        'noplaylist': True,
    }
    
    # 2. تحميل الفيديو
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    # 3. قص الفيديو (سنعتمد هنا توقيت ثابت للتجربة: من 5 إلى 35 ثانية)
    start_time = 5
    end_time = 35
    
    with VideoFileClip("input_video.mp4") as video:
        new = video.subclip(start_time, end_time)
        new.write_videofile("static/output_viral.mp4", codec="libx264", audio_codec="aac")

    return jsonify({
        "success": True,
        "time_frame": f"{start_time} - {end_time}",
        "title": "تم قص الفيديو بنجاح!",
        "tags": "هذا الفيديو تم قصه أوتوماتيكياً بواسطة موقعك! #ViralAI"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
