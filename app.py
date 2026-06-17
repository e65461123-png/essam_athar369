from flask import Flask, render_template_string, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key-change-in-production'

# -------------------- قاعدة البيانات --------------------
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # جدول الرسائل
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        # إضافة مستخدم افتراضي (admin) لو مش موجود
        admin = cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
        if not admin:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                           ('admin', generate_password_hash('123456')))
        db.commit()

# -------------------- Decorator الحماية --------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('⛔ الرجاء تسجيل الدخول أولاً', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -------------------- Routes --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'🎉 مرحباً {user["username"]}!', 'success')
            return redirect(url_for('home'))
        flash('❌ اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    flash('👋 تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('❌ جميع الحقول مطلوبة', 'danger')
            return redirect(url_for('register'))
        db = get_db()
        existing = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            flash('❌ اسم المستخدم موجود بالفعل', 'danger')
            return redirect(url_for('register'))
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                   (username, generate_password_hash(password)))
        db.commit()
        flash('✅ تم التسجيل بنجاح، سجل دخول الآن', 'success')
        return redirect(url_for('login'))
    return render_template_string(REGISTER_TEMPLATE)

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    db = get_db()
    user_id = session['user_id']
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if content:
            db.execute('INSERT INTO messages (user_id, content) VALUES (?, ?)', (user_id, content))
            db.commit()
            flash('✅ تم نشر الرسالة', 'success')
        else:
            flash('❌ الرسالة فارغة', 'danger')
        return redirect(url_for('home'))

    # جلب الرسائل (مع البحث)
    search = request.args.get('search', '')
    if search:
        messages = db.execute('''
            SELECT messages.*, users.username 
            FROM messages JOIN users ON messages.user_id = users.id
            WHERE messages.content LIKE ? OR users.username LIKE ?
            ORDER BY messages.timestamp DESC
        ''', (f'%{search}%', f'%{search}%')).fetchall()
    else:
        messages = db.execute('''
            SELECT messages.*, users.username 
            FROM messages JOIN users ON messages.user_id = users.id
            ORDER BY messages.timestamp DESC
        ''').fetchall()
    
    return render_template_string(HOME_TEMPLATE, messages=messages, search=search)

@app.route('/delete/<int:msg_id>')
@login_required
def delete_message(msg_id):
    db = get_db()
    user_id = session['user_id']
    # التأكد أن الرسالة تخص المستخدم الحالي
    msg = db.execute('SELECT * FROM messages WHERE id = ? AND user_id = ?', (msg_id, user_id)).fetchone()
    if msg:
        db.execute('DELETE FROM messages WHERE id = ?', (msg_id,))
        db.commit()
        flash('🗑️ تم حذف الرسالة', 'info')
    else:
        flash('❌ غير مسموح بالحذف', 'danger')
    return redirect(url_for('home'))

# -------------------- القوالب (HTML مدمجة) --------------------
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>تسجيل الدخول - موقع الأبطال</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #1e1e2f, #2d2d44); min-height: 100vh; display: flex; align-items: center; }
        .card { background: rgba(255,255,255,0.08); backdrop-filter: blur(20px); border: none; border-radius: 30px; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
        .form-control { background: rgba(255,255,255,0.1); border: none; color: #fff; }
        .form-control:focus { background: rgba(255,255,255,0.15); color: #fff; box-shadow: 0 0 0 3px #7f5af0; }
        .btn-primary { background: #7f5af0; border: none; border-radius: 50px; padding: 12px 40px; transition: all 0.3s; }
        .btn-primary:hover { background: #6a4bd0; transform: scale(1.02); }
        .flash { margin-top: 15px; }
        a { color: #7f5af0; text-decoration: none; }
        a:hover { color: #a78bfa; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-5 col-md-7">
                <div class="card text-white p-4 p-md-5">
                    <h2 class="text-center mb-4">🔐 تسجيل الدخول</h2>
                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            {% for category, msg in messages %}
                                <div class="alert alert-{{ category }} alert-dismissible fade show flash" role="alert">
                                    {{ msg }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                </div>
                            {% endfor %}
                        {% endif %}
                    {% endwith %}
                    <form method="POST">
                        <div class="mb-3">
                            <input type="text" name="username" class="form-control" placeholder="اسم المستخدم" required>
                        </div>
                        <div class="mb-3">
                            <input type="password" name="password" class="form-control" placeholder="كلمة المرور" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">🚀 دخول</button>
                    </form>
                    <p class="text-center mt-3">ما عندك حساب؟ <a href="{{ url_for('register') }}">سجل هنا</a></p>
                    <p class="text-center text-muted small">admin / 123456</p>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>تسجيل مستخدم جديد</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #1e1e2f, #2d2d44); min-height: 100vh; display: flex; align-items: center; }
        .card { background: rgba(255,255,255,0.08); backdrop-filter: blur(20px); border: none; border-radius: 30px; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
        .form-control { background: rgba(255,255,255,0.1); border: none; color: #fff; }
        .form-control:focus { background: rgba(255,255,255,0.15); color: #fff; box-shadow: 0 0 0 3px #7f5af0; }
        .btn-primary { background: #7f5af0; border: none; border-radius: 50px; padding: 12px 40px; }
        .btn-primary:hover { background: #6a4bd0; transform: scale(1.02); }
        a { color: #7f5af0; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-5 col-md-7">
                <div class="card text-white p-4 p-md-5">
                    <h2 class="text-center mb-4">✍️ حساب جديد</h2>
                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            {% for category, msg in messages %}
                                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                                    {{ msg }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                </div>
                            {% endfor %}
                        {% endif %}
                    {% endwith %}
                    <form method="POST">
                        <div class="mb-3">
                            <input type="text" name="username" class="form-control" placeholder="اختر اسم مستخدم" required>
                        </div>
                        <div class="mb-3">
                            <input type="password" name="password" class="form-control" placeholder="كلمة المرور" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">🎉 تسجيل</button>
                    </form>
                    <p class="text-center mt-3">عندك حساب؟ <a href="{{ url_for('login') }}">سجل دخول</a></p>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>موقع الأبطال</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #1a1a2e; color: #eee; }
        .navbar { background: #16213e; box-shadow: 0 4px 30px rgba(0,0,0,0.3); }
        .navbar-brand { font-weight: bold; color: #7f5af0 !important; }
        .card { background: #22223b; border: none; border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); transition: transform 0.2s; }
        .card:hover { transform: scale(1.01); }
        .btn-primary { background: #7f5af0; border: none; border-radius: 50px; padding: 10px 25px; }
        .btn-primary:hover { background: #6a4bd0; }
        .btn-danger { border-radius: 50px; }
        .msg { background: #2d2d44; border-radius: 15px; padding: 15px; margin-bottom: 12px; border-left: 5px solid #7f5af0; }
        .msg small { color: #aaa; font-size: 0.8rem; }
        .username { color: #7f5af0; font-weight: bold; }
        .search-box { background: rgba(255,255,255,0.05); border: 1px solid #3a3a55; color: #fff; border-radius: 50px; padding: 10px 20px; }
        .search-box:focus { background: rgba(255,255,255,0.1); color: #fff; box-shadow: 0 0 0 3px #7f5af0; }
        .delete-btn { background: none; border: none; color: #ff6b6b; font-size: 1.1rem; transition: 0.3s; }
        .delete-btn:hover { color: #ff4757; transform: scale(1.2); }
        .flash { margin-top: 10px; border-radius: 50px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container">
            <a class="navbar-brand" href="#"><i class="fas fa-bolt"></i> موقع الأبطال</a>
            <div class="d-flex align-items-center gap-3">
                <span class="text-light"><i class="fas fa-user"></i> {{ session['username'] }}</span>
                <a href="{{ url_for('logout') }}" class="btn btn-outline-danger btn-sm"><i class="fas fa-sign-out-alt"></i> خروج</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, msg in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show flash" role="alert">
                        <i class="fas fa-info-circle"></i> {{ msg }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="row">
            <div class="col-lg-8 mx-auto">
                <div class="card p-4 mb-4">
                    <h5 class="mb-3"><i class="fas fa-pen"></i> اكتب رسالتك</h5>
                    <form method="POST">
                        <div class="input-group">
                            <input type="text" name="content" class="form-control" placeholder="اكتب أي حاجة..." required>
                            <button type="submit" class="btn btn-primary"><i class="fas fa-paper-plane"></i> نشر</button>
                        </div>
                    </form>
                </div>

                <div class="card p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5><i class="fas fa-comments"></i> رسائل الأبطال</h5>
                        <form method="GET" class="d-flex gap-2">
                            <input type="text" name="search" class="search-box" placeholder="🔍 بحث..." value="{{ search }}">
                            <button type="submit" class="btn btn-outline-light btn-sm"><i class="fas fa-search"></i></button>
                        </form>
                    </div>
                    {% if messages %}
                        {% for msg in messages %}
                            <div class="msg">
                                <div class="d-flex justify-content-between">
                                    <span class="username"><i class="fas fa-user-circle"></i> {{ msg['username'] }}</span>
                                    <small><i class="far fa-clock"></i> {{ msg['timestamp'] }}</small>
                                </div>
                                <p class="mt-2">{{ msg['content'] }}</p>
                                {% if msg['user_id'] == session['user_id'] %}
                                    <div class="text-end">
                                        <a href="{{ url_for('delete_message', msg_id=msg['id']) }}" class="delete-btn" onclick="return confirm('احذف الرسالة؟')">
                                            <i class="fas fa-trash-alt"></i>
                                        </a>
                                    </div>
                                {% endif %}
                            </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-muted text-center">✋ مفيش رسايل لسه... كن أول بطل!</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

# -------------------- تشغيل السيرفر --------------------
if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
