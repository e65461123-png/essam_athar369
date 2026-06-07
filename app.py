from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# مهم جدًا لـ Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# 👤 USER MODEL
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    balance = db.Column(db.Float, default=1000.0)

# =========================
# 📊 ORDER MODEL
# =========================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    side = db.Column(db.String(10))  # buy / sell
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    status = db.Column(db.String(20), default="open")
    created = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# ⚡ MATCH ENGINE
# =========================
def match_orders():
    buys = Order.query.filter_by(side="buy", status="open").all()
    sells = Order.query.filter_by(side="sell", status="open").all()

    for b in buys:
        for s in sells:

            if b.price >= s.price and b.status == "open" and s.status == "open":

                trade = min(b.amount, s.amount)

                b.amount -= trade
                s.amount -= trade

                if b.amount <= 0:
                    b.status = "closed"
                if s.amount <= 0:
                    s.status = "closed"

                db.session.commit()

# =========================
# 🏠 HOME (NO HTML FILES)
# =========================
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "PRO EXCHANGE API",
        "routes": ["/register", "/order", "/book"]
    })

# =========================
# 🆕 REGISTER
# =========================
@app.route('/register', methods=['POST'])
def register():

    data = request.json

    user = User(username=data["username"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"status": "user created"})

# =========================
# 📥 PLACE ORDER
# =========================
@app.route('/order', methods=['POST'])
def order():

    data = request.json

    o = Order(
        user=data["user"],
        side=data["side"],
        amount=float(data["amount"]),
        price=float(data["price"])
    )

    db.session.add(o)
    db.session.commit()

    match_orders()

    return jsonify({"status": "order placed"})

# =========================
# 📊 ORDER BOOK
# =========================
@app.route('/book')
def book():

    buys = Order.query.filter_by(side="buy", status="open").all()
    sells = Order.query.filter_by(side="sell", status="open").all()

    return jsonify({
        "buy": [{"price": o.price, "amount": o.amount} for o in buys],
        "sell": [{"price": o.price, "amount": o.amount} for o in sells]
    })

# =========================
# 🔥 INIT DB (SAFE FOR RENDER)
# =========================
with app.app_context():
    db.create_all()

# =========================
# ▶ RUN (IMPORTANT FOR RENDER)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
