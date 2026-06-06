from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# استخدام مسار ثابت لقاعدة البيانات لضمان عدم ضياعها
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'atheer.db')
db = SQLAlchemy(app)

class PlatformData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=1000.0)

with app.app_context():
    db.create_all()
    if not PlatformData.query.first():
        db.session.add(PlatformData(balance=1000.0))
        db.session.commit()

# الواجهة المتكاملة
HTML_PAGE = """
<!DOCTYPE html>
<html dir='rtl'>
<body>
    <h1>منصة ATHEER 369 المالية</h1>
    <h2 id='bal'>الرصيد الحالي: {{ data.balance }}</h2>
    <button onclick='invest()'>استثمار (خصم 10%)</button>
    <hr>
    <h3>المساعد الذكي (AI)</h3>
    <input id='q' placeholder='اسأل الذكاء الاصطناعي...'>
    <button onclick='ask()'>إرسال</button>
    <p id='res'></p>

    <script>
        function invest(){
            fetch('/invest', {method: 'POST'}).then(r => r.json()).then(d => {
                document.getElementById('bal').innerText = 'الرصيد الحالي: ' + d.new_balance;
            });
        }
        function ask(){
            let q = document.getElementById('q').value;
            fetch('/ai', {method: 'POST', body: JSON.stringify({q: q}), headers:{'Content-Type':'application/json'}})
            .then(r => r.json()).then(d => document.getElementById('res').innerText = d.a);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    data = PlatformData.query.first()
    return render_template_string(HTML_PAGE, data=data)

@app.route('/invest', methods=['POST'])
def invest():
    data = PlatformData.query.first()
    data.balance -= (data.balance * 0.10)
    db.session.commit()
    return jsonify({"new_balance": data.balance})

@app.route('/ai', methods=['POST'])
def ai():
    q = request.json.get('q')
    return jsonify({"a": f"مساعد ATHEER: بخصوص '{q}', نحن نقوم الآن بتحليل السوق لضمان أعلى ربح لك."})

if __name__ == '__main__':
    app.run()
