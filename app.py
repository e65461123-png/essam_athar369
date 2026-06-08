from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'aether369_secret_key' # ضروري للجلسات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aether369.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# تعريف الجداول (Models) - لا تحذفها
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

class Wallet(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    balance_usd = db.Column(db.Float, default=0.0)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)

# إنشاء قاعدة البيانات
with app.app_context():
    db.create_all()

# استيراد الـ Blueprints في النهاية (هذا يكسر الـ Circular Import)
from blueprints.routes import main_bp
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
