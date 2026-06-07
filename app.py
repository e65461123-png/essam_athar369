from flask import Flask

# تهيئة التطبيق
app = Flask(__name__)

# استيراد وتجهيز المجلدات الفرعية (Blueprints)
# سنقوم بربطها لاحقاً بمجرد إنشاء الملفات داخل مجلد blueprints
# from blueprints.auth import auth_bp
# app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return "تم التوصيل بنجاح: المشروع يعمل الآن!"

if __name__ == '__main__':
    app.run(debug=True)

