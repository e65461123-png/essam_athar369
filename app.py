from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# إعداد قاعدة البيانات
db_url = os.environ.get("DATABASE_URL", "sqlite:///aether369.db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# تعريف نموذج المستخدم
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, default=369.0)

# إنشاء الجداول
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    user = User.query.first()
    balance = user.balance if user else 369.0
    return render_template('index.html', balance=balance)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
