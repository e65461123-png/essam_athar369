from flask import Flask

app = Flask(__name__)

# هذا المسار يحل مشكلة الـ 404 عند فتح الرابط الرئيسي
@app.route('/')
def home():
    return "🚀 النظام يعمل: مركز القيادة السحابي للقائد الأعلى جاهز."

if __name__ == '__main__':
    app.run()
