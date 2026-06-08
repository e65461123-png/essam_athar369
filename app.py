from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# ... (إعدادات قاعدة البيانات كما هي لديك) ...

@app.route("/")
def home():
    # جلب المستخدم الأول من قاعدة البيانات
    user = User.query.first() 
    # استخدام الرصيد الموجود، أو القيمة الافتراضية 369.0 إذا لم يوجد مستخدم
    balance = user.balance if user else 369.0
    return render_template('index.html', balance=balance)
