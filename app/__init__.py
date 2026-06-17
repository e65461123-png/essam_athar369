from flask import Flask

def create_app():
    app = Flask(__name__)

    # استيراد الـ Blueprints من ملفات الـ routes مباشرة
    from auth.routes import auth_bp
    from main.routes import main_bp

    # تسجيل الـ Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app

