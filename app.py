from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# =====================
# DATABASE SAFE FIX
# =====================
db_url = os.environ.get("DATABASE_URL")

# لو مفيش DB أو فيه Supabase مشاكل → استخدم SQLite
if not db_url or "supabase" in db_url:
    db_url = "sqlite:///aether369.db"

# تحويل postgres القديم
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =====================
# MODEL
# =====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=369.0)

# =====================
# INIT DB
# =====================
with app.app_context():
    db.create_all()

# =====================
# ROUTES
# =====================
@app.route("/")
def home():
    return "AETHER 369 ONLINE ✅"

# =====================
# RUN
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
