from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atheer.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    balance = db.Column(db.Float, default=1000.0)

with app.app_context():
    db.create_all()

# الواجهة الرئيسية (تصميم بسيط وجذاب)
@app.route('/')
def home():
    return render_template_string("""
        <style>body {text-align: center; font-family: sans-serif; background: #f4f4f4;} .card {background: white; padding: 20px; border-radius: 10px; display: inline-block; margin-top: 50px;}</style>
        <div class='card'>
            <h1>ATHEER 369</h1>
            <p>مرحباً بك في منصتك الخاصة</p>
            <button onclick="invest()">استثمار (خصم 10%)</button>
        </div>
        <script>function invest(){fetch('/invest', {method: 'POST'}).then(r=>r.json()).then(d=>alert(d.message))}</script>
    """)

# المحرك المالي
@app.route('/invest', methods=['POST'])
def invest():
    user = User.query.first() # سنربطه لاحقاً بمستخدم حقيقي
    if user:
        user.balance -= (user.balance * 0.10)
        db.session.commit()
        return jsonify({"message": f"تم خصم 10% بنجاح. رصيدك الجديد: {user.balance:.2f}"})
    return jsonify({"message": "خطأ"})

if __name__ == '__main__':
    app.run()
