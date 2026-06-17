from flask import Flask, render_template_string, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-the-earthquake'  # غيرها في الإنتاج

# -------------------- قاعدة بيانات وهمية للمستخدمين --------------------
users = {
    "admin": generate_password_hash("123456"),
    "test": generate_password_hash("test123")
}

# -------------------- تخزين الرسائل في ملف JSON --------------------
DATA_FILE = "messages.json"

def load_msgs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_msgs(msgs):
    with open(DATA_FILE, 'w') as f:
        json.dump(msgs, f, indent=4)

# -------------------- Decorator الحماية --------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -------------------- Routes --------------------

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            return redirect(url_for('home'))
        return "❌ بيانات دخول غلط!"
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>تسجيل الدخول</title>
        <style>
            body { background: #1e1e2f; color: #fff; font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .card { background: #2d2d44; padding: 40px; border-radius: 20px; box-shadow: 0 0 30px #7f5af0; }
            input { display: block; width: 100%; padding: 12px; margin: 10px 0; border-radius: 10px; border: none; }
            button { background: #7f5af0; color: #fff; padding: 12px 30px; border: none; border-radius: 30px; cursor: pointer; }
        </style>
        </head>
        <body>
            <div class="card">
                <h2>🔐 سجل دخول يا بطل</h2>
                <form method="POST">
                    <input type="text" name="username" placeholder="اسم المستخدم" required>
                    <input type="password" name="password" placeholder="كلمة المرور" required>
                    <button type="submit">🚀 دخول</button>
                </form>
                <p style="margin-top: 15px; font-size: 14px;">admin / 123456 أو test / test123</p>
            </div>
        </body>
        </html>
    ''')

# صفحة الخروج
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# الصفحة الرئيسية (محمية)
@app.route('/')
@login_required
def home():
    msgs = load_msgs()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>🔥 موقع الأبطال</title>
        <style>
            body { font-family: Arial; background: #1e1e2f; color: #fff; text-align: center; padding: 50px; }
            .card { background: #2d2d44; padding: 30px; border-radius: 20px; max-width: 600px; margin: auto; box-shadow: 0 0 30px #7f5af0; }
            input, textarea { width: 90%; padding: 12px; margin: 10px 0; border-radius: 10px; border: none; }
            button { background: #7f5af0; color: #fff; padding: 12px 30px; border: none; border-radius: 30px; cursor: pointer; }
            .msg { background: #3a3a55; margin: 10px 0; padding: 15px; border-radius: 15px; text-align: left; }
            .timestamp { font-size: 12px; color: #aaa; }
            a { color: #7f5af0; text-decoration: none; }
            .logout { color: #ff6b6b; }
        </style>
        </head>
        <body>
            <div class="card">
                <h1>🚀 مرحباً يا {{ session['user'] }}!</h1>
                <p>الموقع بقى محمي ومتطور 😎</p>
                <hr>
                <h3>💬 سيب رسالتك:</h3>
                <form method="POST">
                    <input type="text" name="user" placeholder="اسمك" required><br>
                    <textarea name="content" rows="3" placeholder="اكتب أي حاجة..."></textarea><br>
                    <button type="submit">💥 انشر الرسالة</button>
                </form>
                <hr>
                <h3>📜 رسائل الأبطال:</h3>
                {% if msgs %}
                    {% for m in msgs %}
                        <div class="msg">
                            <strong>{{ m.user }}</strong>: {{ m.content }}
                            <div class="timestamp">🕒 {{ m.timestamp }}</div>
                        </div>
                    {% endfor %}
                {% else %}
                    <p>✋ مفيش رسائل لسه، كن أول بطل!</p>
                {% endif %}
                <br>
                <a href="{{ url_for('clear') }}">🗑️ مسح الكل</a> |
                <a href="{{ url_for('logout') }}" class="logout">🚪 تسجيل خروج</a>
            </div>
        </body>
        </html>
    ''', msgs=msgs)

# مسح الرسائل (محمي)
@app.route('/clear')
@login_required
def clear():
    save_msgs([])
    return redirect(url_for('home'))

# معالجة إضافة رسالة جديدة (POST)
@app.route('/', methods=['POST'])
@login_required
def add_message():
    msgs = load_msgs()
    user = request.form.get('user', '').strip()
    content = request.form.get('content', '').strip()
    if user and content:
        msgs.append({
            "user": user,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_msgs(msgs)
    return redirect(url_for('home'))

# -------------------- تشغيل السيرفر --------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
