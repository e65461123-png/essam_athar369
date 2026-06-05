from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# إعداد قاعدة بيانات محلية (ستعمل على Render)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atheer369.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# نموذج المستخدم (الرصيد)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=1000.0)

# إنشاء قاعدة البيانات
with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(balance=1000.0))
        db.session.commit()

# واجهة المستخدم (المنصة)
@app.route('/')
def home():
    user = User.query.first()
    return render_template_string("""
        <div style="text-align:center; margin-top:50px;">
            <h1>ATHEER 369</h1>
            <h2 id="balance">الرصيد: {{ user.balance }}</h2>
            <button onclick="invest()" style="padding:10px 20px;">استثمار (خصم 10%)</button>
        </div>
        <script>
            function invest() {
                fetch('/invest', {method: 'POST'})
                .then(r => r.json())
                .then(d => {
                    document.getElementById('balance').innerText = 'الرصيد: ' + d.new_balance;
                    alert(d.message);
                });
            }
        </script>
    """, user=user)

# المحرك المالي (العملية الحقيقية)
@app.route('/invest', methods=['POST'])
def invest():
    user = User.query.first()
    deduction = user.balance * 0.10
    user.balance -= deduction
    db.session.commit()
    return jsonify({"message": f"تم خصم 10% بنجاح!", "new_balance": f"{user.balance:.2f}"})

if __name__ == '__main__':
    app.run()
