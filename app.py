import os
import logging
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

# ==================== الإعدادات الأساسية ====================
app = Flask(__name__)

# حد أقصى لحجم الطلب (16 ميجابايت) لمنع استهلاك الذاكرة
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# إعداد نظام التسجيل (السجلات)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==================== قاعدة البيانات ====================
DB_NAME = 'radar.db'

def init_db():
    """إنشاء جدول السجلات إذا لم يكن موجوداً مسبقاً"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS radar_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            value TEXT NOT NULL,
            raw_data TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("✅ تم تهيئة قاعدة البيانات بنجاح.")

# تشغيل تهيئة قاعدة البيانات عند بدء الخادم
init_db()

# ==================== المسارات (Routes) ====================

@app.route('/')
def home():
    """الصفحة الرئيسية للتحقق من أن الخادم يعمل"""
    return "🚀 النظام يعمل: مركز القيادة السحابي للقائد الأعلى جاهز."


@app.route('/report', methods=['POST'])
def report():
    """
    استقبال تقارير الرادار (POST).
    يتطلب JSON يحتوي على حقلي 'source' و 'value' على الأقل.
    """
    try:
        # 1. التحقق من صحة JSON
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "الطلب يجب أن يكون بصيغة JSON"}), 400

        # 2. التحقق من الحقول المطلوبة
        source = data.get('source')
        value = data.get('value')
        if source is None or value is None:
            return jsonify({
                "error": "الحقول المطلوبة مفقودة. يجب إرسال 'source' و 'value'"
            }), 400

        # 3. تخزين البيانات في قاعدة البيانات (وليس في الذاكرة)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO radar_logs (timestamp, source, value, raw_data) VALUES (?, ?, ?, ?)",
            (datetime.utcnow().isoformat(), str(source), str(value), str(data))
        )
        conn.commit()
        conn.close()

        logging.info(f"📡 إشارة جديدة رُصِدت: المصدر={source}, القيمة={value}")
        return jsonify({"status": "received", "message": "تم استقبال التقرير بنجاح"}), 200

    except Exception as e:
        logging.error(f"⚠️ خطأ في المعالجة: {e}")
        return jsonify({"error": "حدث خطأ داخلي في الخادم"}), 500


@app.route('/logs', methods=['GET'])
def get_logs():
    """
    عرض آخر 100 سجل (مع مصادقة بمفتاح API).
    أضف المفتاح في رأس الطلب: X-API-Key: your_secret_key
    """
    # 🔐 المصادقة: اقرأ المفتاح من البيئة، أو استخدم القيمة الافتراضية للتجربة
    expected_api_key = os.environ.get('ADMIN_API_KEY', 'secure-default-key-change-me')
    received_key = request.headers.get('X-API-Key')

    if not received_key or received_key != expected_api_key:
        logging.warning("🚫 محاولة وصول غير مصرح بها إلى /logs")
        return jsonify({"error": "غير مصرح به. تأكد من إرسال X-API-Key صحيح"}), 401

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # جلب آخر 100 سجل، مرتبة من الأحدث إلى الأقدم
        c.execute(
            "SELECT timestamp, source, value, raw_data FROM radar_logs ORDER BY id DESC LIMIT 100"
        )
        rows = c.fetchall()
        conn.close()

        # تنسيق النتيجة كقائمة JSON
        logs_list = [
            {
                "timestamp": row[0],
                "source": row[1],
                "value": row[2],
                "raw_data": row[3]
            }
            for row in rows
        ]
        return jsonify(logs_list), 200

    except Exception as e:
        logging.error(f"⚠️ خطأ في قراءة السجلات: {e}")
        return jsonify({"error": "حدث خطأ في قراءة قاعدة البيانات"}), 500


# ==================== تشغيل الخادم ====================
if __name__ == '__main__':
    # القراءة من متغيرات البيئة لتسهيل النشر (مثل منصة Render أو Railway)
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))

    logging.info(f"🔥 تشغيل الخادم على {host}:{port}")
    app.run(host=host, port=port, debug=False)  # debug=False في الإنتاج
