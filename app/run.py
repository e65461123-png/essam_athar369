from flask import Flask
import os

def create_app():
    # نحدد المسارات بحيث يبحث في المجلدات التي نقلناها داخل app
    app = Flask(__name__, 
                template_folder='templates', 
                static_folder='static')
    
    # هنا يمكنك إضافة إعدادات قاعدة البيانات أو الـ Blueprints لاحقاً
    return app
