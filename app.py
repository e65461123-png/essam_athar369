from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'final-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# 👤 USER MODEL
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    balance = db.Column(db.Float, default=1000.0)
    role = db.Column(db.String(20), default="user")

# =========================
# 📊 ORDERS (BUY/SELL)
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
# 🏠 HOME UI (MERGED)
# =========================
@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Trading Platform</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-dark text-white text-center">

        <h1 class="mt-5">📈 Trading Platform</h1>

        <p>💰 Secure Exchange Core System</p>

        <div class="mt-4">
            <a class="btn btn-success m-2" href="/buy">Buy</a>
            <a class="btn btn-danger m-2" href="/sell">Sell</a>
            <a class="btn btn-primary m-2" href="/orders">Orders</a>
        </div>

    </body>
    </html>
    """

# =========================
# 🟢 BUY ORDER
# =========================
@app.route('/buy', methods=['GET','POST'])
def buy():
    if request.method == 'POST':
        order = Order(
            user=session.get('user','guest'),
            type="buy",
            amount=float(request.form['amount']),
            price=float(request.form['price'])
        )
        db.session.add(order)
        db.session.commit()

        match_orders()
        return redirect('/orders')

    return """
    <h2>Buy Order</h2>
    <form method='post'>
        <input name='amount' placeholder='Amount'><br>
        <input name='price' placeholder='Price'><br>
        <button>Submit Buy</button>
    </form>
    """

# =========================
# 🔴 SELL ORDER
# =========================
@app.route('/sell', methods=['GET','POST'])
def sell():
    if request.method == 'POST':
        order = Order(
            user=session.get('user','guest'),
            type="sell",
            amount=float(request.form['amount']),
            price=float(request.form['price'])
        )
        db.session.add(order)
        db.session.commit()

        match_orders()
        return redirect('/orders')

    return """
    <h2>Sell Order</h2>
    <form method='post'>
        <input name='amount'><br>
        <input name='price'><br>
        <button>Submit Sell</button>
    </form>
    """

# =========================
# ⚡ MATCHING ENGINE
# =========================
def match_orders():
    buys = Order.query.filter_by(type="buy", status="open").all()
    sells = Order.query.filter_by(type="sell", status="open").all()

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
# 📊 ORDERS PAGE
# =========================
@app.route('/orders')
def orders():
    data = Order.query.all()

    html = "<h2>📊 Orders</h2>"
    for o in data:
        html += f"<p>{o.user} | {o.type} | {o.amount} | {o.price} | {o.status}</p>"

    html += "<br><a href='/'>Back</a>"
    return html

# =========================
# 🔐 INIT DB + ADMIN
# =========================
def create_admin():
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
            balance=999999,
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_admin()

# =========================
# ▶ RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
