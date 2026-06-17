from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'

    # استيراد الـ Blueprints من المسار الصحيح
    from auth.routes import auth_bp
    from main.routes import main_bp

    # تسجيل الـ Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
