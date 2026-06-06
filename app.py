from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pro-exchange-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pro.db'
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
# 🏠 DASHBOARD (PRO UI)
# =========================
@app.route('/')
def dashboard():
    orders = Order.query.order_by(Order.id.desc()).all()

    buy_orders = [o for o in orders if o.type == "buy"]
    sell_orders = [o for o in orders if o.type == "sell"]

    buy_html = "".join([f"<tr><td>{o.amount}</td><td>{o.price}</td></tr>" for o in buy_orders])
    sell_html = "".join([f"<tr><td>{o.amount}</td><td>{o.price}</td></tr>" for o in sell_orders])

    return f"""
    <html>
    <head>
        <title>PRO Exchange</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

        <style>
            body {{ background:#0f172a; color:white; }}
            .card {{ background:#1e293b; border:none; }}
            table {{ color:white; }}
        </style>
    </head>

    <body>

    <div class="container mt-4">

        <h2>📈 PRO TRADING DASHBOARD</h2>
        <p>💰 Live Order Book System</p>

        <div class="row">

            <div class="col-md-4">
                <div class="card p-3">
                    <h4>🟢 Buy Orders</h4>
                    <table class="table">
                        <tr><th>Amount</th><th>Price</th></tr>
                        {buy_html}
                    </table>
                </div>
            </div>

            <div class="col-md-4 text-center">
                <a class="btn btn-success m-2" href="/buy">BUY</a>
                <a class="btn btn-danger m-2" href="/sell">SELL</a>
            </div>

            <div class="col-md-4">
                <div class="card p-3">
                    <h4>🔴 Sell Orders</h4>
                    <table class="table">
                        <tr><th>Amount</th><th>Price</th></tr>
                        {sell_html}
                    </table>
                </div>
            </div>

        </div>

        <a href="/orders" class="btn btn-primary mt-3">Full Orders</a>

    </div>

    </body>
    </html>
    """

# =========================
# 🟢 BUY
# =========================
@app.route('/buy', methods=['GET','POST'])
def buy():
    if request.method == 'POST':
        o = Order(
            user="user",
            type="buy",
            amount=float(request.form['amount']),
            price=float(request.form['price'])
        )
        db.session.add(o)
        db.session.commit()
        match()
        return redirect('/')

    return """
    <form method='post'>
        <input name='amount' placeholder='Amount'><br>
        <input name='price' placeholder='Price'><br>
        <button>Buy</button>
    </form>
    """

# =========================
# 🔴 SELL
# =========================
@app.route('/sell', methods=['GET','POST'])
def sell():
    if request.method == 'POST':
        o = Order(
            user="user",
            type="sell",
            amount=float(request.form['amount']),
            price=float(request.form['price'])
        )
        db.session.add(o)
        db.session.commit()
        match()
        return redirect('/')

    return """
    <form method='post'>
        <input name='amount'><br>
        <input name='price'><br>
        <button>Sell</button>
    </form>
    """

# =========================
# ⚡ MATCH ENGINE
# =========================
def match():
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
# 📊 ALL ORDERS
# =========================
@app.route('/orders')
def orders():
    data = Order.query.all()
    html = "<h2>📊 All Orders</h2>"

    for o in data:
        html += f"<p>{o.user} | {o.type} | {o.amount} | {o.price} | {o.status}</p>"

    html += "<a href='/'>Back</a>"
    return html

# =========================
# 🔥 INIT
# =========================
with app.app_context():
    db.create_all()

# =========================
# ▶ RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
