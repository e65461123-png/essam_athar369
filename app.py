from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# إنشاء تطبيق Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "AETHER369_SECRET_KEY")

# إعداد قاعدة البيانات
db_url = os.environ.get("DATABASE_URL", "sqlite:///aether369.db")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
