from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # تحديد مسار قاعدة البيانات
    app.config['DATABASE'] = os.path.join(app.instance_path, 'archive.db')
    
    # التأكد من وجود مجلد instance
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # تسجيل المسارات (Blueprints)
    from main.routes import main_bp
    app.register_blueprint(main_bp)
    
    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    
    return app
