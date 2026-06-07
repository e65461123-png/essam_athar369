from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# =========================
# 🔥 FIX: DATABASE CONFIG
# =========================
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///app.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# TEST ROUTE
# =========================
@app.route("/")
def home():
    return "✅ SERVER RUNNING SUCCESSFULLY"

# =========================
# INIT DB
# =========================
with app.app_context():
    db.create_all()

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
