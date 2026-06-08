from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()

# دالة لجلب سعر البيتكوين
def get_btc_price():
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
        return round(float(response.json()['price']), 2)
    except:
        return "غير متاح حالياً"

@app.route('/')
def home():
    price = get_btc_price()
    content = f"<h2>سعر البيتكوين الآن: {price} $</h2><a href='/register'>إنشاء حساب</a> | <a href='/login'>دخول</a>"
    return render_template_string(layout, content=content)

layout = """
<div style="text-align:center; padding-top:50px; font-family:Tahoma; background:#0f172a; color:white; min-height:100vh;">
    <h1>AETHER 369</h1>
    <div style="width:300px; margin:auto; background:#1e293b; padding:20px; border-radius:15px;">
        {{ content | safe }}
    </div>
</div>
"""
# (أضف دالتي register و login السابقتين هنا كما هما)
# ... (باقي كود register و login هنا)
