from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
# ... (نفس إعدادات قاعدة البيانات السابقة) ...

# الواجهة العالمية (Dark Dashboard Style)
layout = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0f172a; color: white; font-family: 'Segoe UI', sans-serif; }
        .card { background-color: #1e293b; border: none; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .btn-primary { background: linear-gradient(90deg, #3b82f6, #8b5cf6); border: none; }
    </style>
</head>
<body class="d-flex align-items-center justify-content-center min-vh-100">
    <div class="card p-4 text-center" style="width: 400px;">
        <h2 class="mb-4">AETHER 369</h2>
        {{ content | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # جلب السعر مع تصميم احترافي
    price = get_btc_price()
    content = f"<h4 class='text-primary'>سعر البيتكوين</h4><h2 class='display-6'>{price} $</h2><hr><a href='/register' class='btn btn-primary w-100 mb-2'>إنشاء حساب</a><a href='/login' class='btn btn-outline-light w-100'>تسجيل الدخول</a>"
    return render_template_string(layout, content=content)

# ... (باقي دوال التسجيل والدخول بنفس التنسيق) ...
