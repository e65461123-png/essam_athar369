from flask import Flask
from blueprints.routes import main_bp
from models.database import db

app = Flask(__name__)

# إعداد قاعدة بيانات محلية (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aether.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ربط الـ db بالتطبيق
db.init_app(app)

# تسجيل الـ Blueprint
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
