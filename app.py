from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'trade-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# 👤 USER
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    balance = db.Column(db.Float, default=1000.0)

# =========================
# 📊 ORDER BOOK
# =========================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    type = db.Column(db.String(10))  # buy / sell
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    status = db.Column(db.String(20), default="open")
    created = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# 🏠 HOME
# =========================
@app.route('/')
def home():
    return """
    <h2>📈 Trading Platform</h2>
    <a href='/buy'>Buy</a> |
    <a href='/sell'>Sell</a> |
    <a href='/orders'>Orders</a>
    """

# =========================
# 🟢 BUY ORDER
# =========================
@app.route('/buy', methods=['GET','POST'])
def buy():
    if request.method == 'POST':
        user = session['user']
        amount = float(request.form['amount'])
        price = float(request.form['price'])

        order = Order(user=user, type="buy", amount=amount, price=price)
        db.session.add(order)
        db.session.commit()

        match_orders()
        return redirect('/orders')

    return """
    <form method='post'>
        <input name='amount' placeholder='Amount'>
        <input name='price' placeholder='Price'>
        <button>Buy</button>
    </form>
    """

# =========================
# 🔴 SELL ORDER
# =========================
@app.route('/sell', methods=['GET','POST'])
def sell():
    if request.method == 'POST':
        user = session['user']
        amount = float(request.form['amount'])
        price = float(request.form['price'])

        order = Order(user=user, type="sell", amount=amount, price=price)
        db.session.add(order)
        db.session.commit()

        match_orders()
        return redirect('/orders')

    return """
    <form method='post'>
        <input name='amount' placeholder='Amount'>
        <input name='price' placeholder='Price'>
        <button>Sell</button>
    </form>
    """

# =========================
# ⚡ MATCHING ENGINE (CORE)
# =========================
def match_orders():
    buys = Order.query.filter_by(type="buy", status="open").all()
    sells = Order.query.filter_by(type="sell", status="open").all()

    for b in buys:
        for s in sells:
            if b.price >= s.price and b.status == "open" and s.status == "open":

                trade_amount = min(b.amount, s.amount)

                b.amount -= trade_amount
                s.amount -= trade_amount

                if b.amount == 0:
                    b.status = "closed"
                if s.amount == 0:
                    s.status = "closed"

                db.session.commit()

# =========================
# 📊 ORDERS PAGE
# =========================
@app.route('/orders')
def orders():
    data = Order.query.all()

    out = ""
    for o in data:
        out += f"<p>{o.user} | {o.type} | {o.amount} | {o.price} | {o.status}</p>"

    return out

# =========================
# 🔐 INIT
# =========================
with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
            balance=999999
        )
        db.session.add(admin)
        db.session.commit()

# =========================
# ▶ RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
