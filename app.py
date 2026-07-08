from flask import Flask, render_template, request, jsonify, redirect, session, send_file
import sqlite3
import hashlib
import random
import subprocess
import os
import json
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.secret_key = "EssamElkomy369"

# ====================================================
#  🗄️ قاعدة البيانات
# ====================================================
def init_db():
    conn = sqlite3.connect('ai_builder.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        balance INTEGER DEFAULT 0,
        level TEXT DEFAULT 'Basic'
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_balance INTEGER DEFAULT 0,
        last_transfer TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS osint_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        report TEXT,
        time TEXT
    )''')
    c.execute("SELECT * FROM vault")
    if not c.fetchone():
        c.execute("INSERT INTO vault (total_balance, last_transfer) VALUES (0, 'لم يتم التحويل بعد')")
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, email, balance, level) VALUES (?, ?, ?, ?, ?)",
                  ('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'e65461123@gmail.com', 1000, 'Admin'))
    conn.commit()
    conn.close()

init_db()

# ====================================================
#  🧠 دوال المساعدة
# ====================================================
def get_user(username):
    conn = sqlite3.connect('ai_builder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect('ai_builder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def get_vault():
    conn = sqlite3.connect('ai_builder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM vault")
    vault = c.fetchone()
    conn.close()
    return vault

def update_vault(amount):
    conn = sqlite3.connect('ai_builder.db')
    c = conn.cursor()
    c.execute("UPDATE vault SET total_balance = total_balance + ?", (amount,))
    conn.commit()
    conn.close()

def transfer_to_bank(amount):
    conn = sqlite3.connect('ai_builder.db')
    c = conn.cursor()
    c.execute("UPDATE vault SET total_balance = 0, last_transfer = ?", (datetime.now().strftime("%Y-%m-%d %H:%M"),))
    conn.commit()
    conn.close()
    return f"✅ تم تحويل {amount} دولار إلى الحساب البنكي!"

def save_osint_report(phone, report):
    conn = sqlite3.connect('ai_builder.db')
    c = conn.cursor()
    c.execute("INSERT INTO osint_reports (phone, report, time) VALUES (?, ?, ?)",
              (phone, report, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_osint_reports(phone=None):
    conn = sqlite3.connect('ai_builder.db')
    c = conn.cursor()
    if phone:
        c.execute("SELECT * FROM osint_reports WHERE phone = ? ORDER BY time DESC", (phone,))
    else:
        c.execute("SELECT * FROM osint_reports ORDER BY time DESC")
    reports = c.fetchall()
    conn.close()
    return reports

# ====================================================
#  🤖 الذكاء الاصطناعي
# ====================================================
def ai_response(question):
    responses = [
        "🔮 تحليل المشكلة: أنت بحاجة إلى التركيز على الأولويات.",
        "🧠 الذكاء الاصطناعي يقترح: حل المشكلة يبدأ من الخطوة الأولى.",
        "💡 نصيحة ذكية: المستقبل يحتاج إلى قرارات جريئة.",
        "🌟 EssamElkomy 369 ينصحك: لا تنتظر الفرصة، اصنعها.",
        "📊 تحليل البيانات: هناك 85% احتمالية للنجاح إذا بدأت الآن.",
        "⚡ توصية: ركز على تطوير مهاراتك الرقمية.",
        "🛸 رسالة من المستقبل: الحل أقرب مما تتصور.",
        "💰 المال قادم إليك.. لكن عليك اتخاذ الخطوة الأولى."
    ]
    return random.choice(responses)

# ====================================================
#  🕵️ نظام الاستطلاع (OSINT) - الجسر البرمجي
# ====================================================
REPORTS_DIR = "reports"
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

def run_osint_master(phone):
    """تشغيل سكربت osint_master.sh على رقم الهاتف"""
    result = {
        "phone": phone,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "output": "",
        "error": "",
        "report_content": ""
    }
    
    # البحث عن مسار osint_master.sh
    script_paths = [
        "~/osint_master.sh",
        "~/X-osint/osint_master.sh",
        "./osint_master.sh"
    ]
    
    script_found = None
    for path in script_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            script_found = expanded_path
            break
    
    if not script_found:
        result["error"] = "❌ سكربت osint_master.sh غير موجود!"
        result["report_content"] = "⚠️ لم يتم العثور على السكربت"
        return result
    
    # تشغيل السكربت
    try:
        process = subprocess.Popen(
            ["bash", script_found, phone],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(script_found)
        )
        stdout, stderr = process.communicate(timeout=60)
        result["output"] = stdout
        result["error"] = stderr
    except subprocess.TimeoutExpired:
        process.kill()
        result["error"] = "⚠️ الوقت انتهى (60 ثانية)"
    except Exception as e:
        result["error"] = f"❌ خطأ: {str(e)}"
    
    # قراءة ملف التقرير
    report_file = "ghost_report.txt"
    if os.path.exists(report_file):
        with open(report_file, "r") as f:
            result["report_content"] = f.read()
    else:
        result["report_content"] = "⚠️ لم يتم إنشاء تقرير"
    
    # حفظ التقرير في قاعدة البيانات
    save_osint_report(phone, result["report_content"])
    
    # حفظ التقرير كـ JSON
    json_file = f"{REPORTS_DIR}/report_{phone}_{int(time.time())}.json"
    with open(json_file, "w") as f:
        json.dump(result, f, indent=4)
    
    return result

# ====================================================
#  🌐 صفحات الموقع
# ====================================================
@app.route('/')
def home():
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        return render_template('index.html', username=user[1], balance=user[4], level=user[5])
    return render_template('index.html', username='زائر', balance=0, level='Basic')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if user and user[2] == hashlib.sha256(password.encode()).hexdigest():
            session['user_id'] = user[0]
            return redirect('/')
        return "❌ اسم المستخدم أو كلمة السر غلط!"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        if get_user(username):
            return "❌ هذا الاسم موجود!"
        conn = sqlite3.connect('ai_builder.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                  (username, hashlib.sha256(password.encode()).hexdigest(), email))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/admin_panel')
def admin_panel():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    if user[5] != 'Admin':
        return "❌ غير مصرح لك"
    vault = get_vault()
    conn = sqlite3.connect('ai_builder.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    html = """
    <h1>⚙️ لوحة التحكم الخاصة</h1>
    <h2>💰 الخزنة السرية</h2>
    <p>إجمالي الأرباح: <strong>{} دولار</strong></p>
    <p>آخر تحويل: {}</p>
    <form method="POST" action="/transfer">
        <button type="submit">تحويل الأرباح للحساب البنكي</button>
    </form>
    <h2>👥 المستخدمين</h2>
    <ul>
    """.format(vault[1], vault[2])
    for u in users:
        html += f"<li>{u[1]} - رصيد: {u[4]} - مستوى: {u[5]} - بريد: {u[3]}</li>"
    html += "</ul><a href='/'>🏠 العودة</a>"
    return html

@app.route('/transfer', methods=['POST'])
def transfer():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    if user[5] != 'Admin':
        return "❌ غير مصرح لك"
    vault = get_vault()
    if vault[1] == 0:
        return "❌ لا توجد أرباح للتحويل"
    result = transfer_to_bank(vault[1])
    return result + "<br><a href='/admin_panel'>العودة للوحة التحكم</a>"

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = ai_response(question)
        return jsonify({'answer': answer})
    return render_template('chat.html')

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        amount = int(request.form.get('amount'))
        if amount <= 0:
            return "❌ المبلغ يجب أن يكون أكبر من 0"
        conn = sqlite3.connect('ai_builder.db')
        c = conn.cursor()
        c.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, session['user_id']))
        conn.commit()
        conn.close()
        update_vault(amount)
        return f"✅ تم شحن {amount} دولار بنجاح!"
    return render_template('pay.html')

# ====================================================
#  🕵️ نظام الاستطلاع (OSINT) - API Endpoints
# ====================================================
@app.route('/osint', methods=['GET', 'POST'])
def osint():
    if request.method == 'POST':
        phone = request.form.get('phone')
        if not phone:
            return "❌ من فضلك أدخل رقم الهاتف"
        
        # تشغيل السكربت
        result = run_osint_master(phone)
        
        # عرض النتائج
        html = f"""
        <h1>🕵️ تقرير الاستطلاع</h1>
        <p><strong>رقم الهاتف:</strong> {phone}</p>
        <p><strong>التاريخ:</strong> {result['time']}</p>
        <hr>
        <h2>📄 محتوى التقرير</h2>
        <pre>{result['report_content']}</pre>
        <hr>
        <h2>📤 مخرجات السكربت</h2>
        <pre>{result['output'][:2000] if result['output'] else 'لا يوجد مخرجات'}</pre>
        <hr>
        <h2>⚠️ الأخطاء</h2>
        <pre>{result['error'] if result['error'] else 'لا توجد أخطاء'}</pre>
        <hr>
        <a href="/">🏠 العودة للرئيسية</a>
        """
        return html
    
    return '''
    <h1>🕵️ نظام الاستطلاع (OSINT)</h1>
    <form method="POST">
        <input type="text" name="phone" placeholder="أدخل رقم الهاتف...">
        <button type="submit">🔍 استطلاع</button>
    </form>
    <a href="/">🏠 العودة للرئيسية</a>
    '''

@app.route('/reports')
def reports():
    reports = get_osint_reports()
    html = "<h1>📊 التقارير السابقة</h1><ul>"
    for r in reports:
        html += f"<li>{r[1]} - {r[3]}</li>"
    html += "</ul><a href='/'>🏠 العودة</a>"
    return html

@app.route('/store')
def store():
    return "🛒 المتجر - قريباً"

@app.route('/courses')
def courses():
    return "🎓 الدورات - قريباً"

@app.route('/crypto')
def crypto():
    return "💎 العملات الرقمية - قريباً"

@app.route('/live')
def live():
    return "📡 البث المباشر - قريباً"

@app.route('/marketing')
def marketing():
    return "📢 التسويق الذكي - قريباً"

@app.route('/support')
def support():
    return "🛠️ الدعم الفني - قريباً"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 - الصفحة غير موجودة</h1><a href='/'>🏠 العودة للرئيسية</a>", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
