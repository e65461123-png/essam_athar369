
#!/usr/bin/env bash
# تحديث وتثبيت مكتبة ffmpeg الضرورية لقص الفيديوهات
apt-get update
apt-get install -y ffmpeg
# تثبيت المكتبات المطلوبة
pip install -r requirements.txt
