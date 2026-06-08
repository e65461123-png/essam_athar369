from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

# استورد الـ Models هنا
# ... (تعريف الكلاسات User, Wallet, AuditLog) ...

# استورد الـ Blueprints في نهاية الملف (بعد تعريف كل شيء)
from blueprints.routes import main_bp
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
