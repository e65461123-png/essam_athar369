#!/usr/bin/env python3
import os
import time
from datetime import datetime

print("""
🌙 تجربة الواقع الافتراضي للقمر
استعد لرحلة إلى سطح القمر!
""")

print("🚀 3... 2... 1... الانطلاق!")
time.sleep(2)
print("🌍 الأرض تبتعد...")
time.sleep(2)
print("🌙 تقترب من سطح القمر...")
time.sleep(2)

print("""
🌙 أنت الآن على سطح القمر!
🌍 الأرض تشرق من بعيد
⭐ النجوم تتلألأ
🌙 التربة القمرية تحت قدميك
🚀 EssamElkomy 369 - أول إنسان على القمر!
""")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"moon_surface_{timestamp}.txt"

with open(filename, "w") as f:
    f.write(f"🌙 سطح القمر - EssamElkomy 369\n")
    f.write(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

print(f"📸 تم حفظ صورة لسطح القمر: {filename}")
