from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atheer_core.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# نظام الحماية (تحديد معدل الطلبات لمنع الـ DDoS)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# نماذج قاعدة البيانات (المستخدمين والمحفظة)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    balance = db.Column(db.Float, default=1000.0)
    profit = db.Column(db.Float, default=0.0)

with app.app_context():
    db.create_all()

# واجهة المنصة (تحتوي على كل الخصائص)
HTML_CORE = """
<!DOCTYPE html>
<html dir='rtl'>
<head><title>ATHEER 369 | المنصة المالية</title></head>
<body style='font-family: sans-serif; text-align: center; background: #0f0f0f; color: white;'>
    <h1>منصة ATHEER 369 الذكية</h1>
    <div id='wallet'>الرصيد: {{ user.balance }} | الأرباح: {{ user.profit }}</div>
    <button onclick='invest()'>استثمار (نظام التحوط الذكي)</button>
    <hr>
    <h3>المساعد الآلي (AI Support)</h3>
    <input type='text' id='ai-input' placeholder='اسأل مساعدك الذكي...'>
    <button onclick='askAI()'>إرسال</button>
    <p id='ai-response'></p>
    
    <script>
        function invest(){
            fetch('/invest', {method: 'POST'}).then(r => r.json()).then(d => location.reload());
        }
        function askAI(){
            let query = document.getElementById('ai-input').value;
            fetch('/ai', {method: 'POST', body: JSON.stringify({query: query}), headers:{'Content-Type': 'application/json'}})
            .then(r => r.json()).then(d => document.getElementById('ai-response').innerText = d.answer);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    user = User.query.first() or User(username='Admin')
    return render_template_string(HTML_CORE, user=user)

@app.route('/invest', methods=['POST'])
@limiter.limit("5 per minute")
def invest():
    user = User.query.first()
    # المحرك المالي: منطق الاستثمار والتحوط
    investment = user.balance * 0.10
    user.balance -= investment
    user.profit += (investment * 1.2) # نسبة ربح محاكية
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/ai', methods=['POST'])
def ai_chat():
    # هذا هو مكان دمج الـ AI (الرد الآلي)
    data = request.json
    return jsonify({"answer": f"مساعد ATHEER: لقد فهمت طلبك بخصوص '{data['query']}', المنصة تعمل بنظام تحوط ذكي لحماية رصيدك."})

if __name__ == '__main__':
    app.run()
