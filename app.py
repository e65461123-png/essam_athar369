from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'exchange-pro'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exchange.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# 👤 USERS
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    balance = db.Column(db.Float, default=1000.0)

# =========================
# 📊 ORDERS
# =========================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    type = db.Column(db.String(10))  # buy / sell
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    status = db.Column(db.String(20), default="open")

# =========================
# ⚡ MATCH ENGINE (REAL CORE)
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
# 🏠 DASHBOARD (LIVE VIEW)
# =========================
@app.route('/')
def home():

    orders = Order.query.all()

    buy_html = ""
    sell_html = ""

    for o in orders:
        row = f"<tr><td>{o.amount}</td><td>{o.price}</td><td>{o.status}</td></tr>"

        if o.type == "buy":
            buy_html += row
        else:
            sell_html += row

    return f"""
    <html>
    <head>
        <title>PRO EXCHANGE</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-dark text-white text-center">

        <h1 class="mt-4">📈 PRO MINI EXCHANGE</h1>
        <p>💰 Live Matching Engine System</p>

        <div class="mt-3">
            <a class="btn btn-success m-2" href="/buy">BUY</a>
            <a class="btn btn-danger m-2" href="/sell">SELL</a>
        </div>

        <div class="container mt-4 row">

            <div class="col-md-6">
                <h3>🟢 BUY ORDERS</h3>
                <table class="table table-dark">
                    <tr><th>Amount</th><th>Price</th><th>Status</th></tr>
                    {buy_html}
                </table>
            </div>

            <div class="col-md-6">
                <h3>🔴 SELL ORDERS</h3>
                <table class="table table-dark">
                    <tr><th>Amount</th><th>Price</th><th>Status</th></tr>
                    {sell_html}
                </table>
            </div>

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
        o = Order(
            user="user",
            type="buy",
            amount=float(request.form['amount']),
            price=float(request.form['price'])
        )
        db.session.add(o)
        db.session.commit()

        match_orders()
        return redirect('/')

    return """
    <h2>Buy Order</h2>
    <form method='post'>
        <input name='amount' placeholder='Amount'><br><br>
        <input name='price' placeholder='Price'><br><br>
        <button>Submit Buy</button>
    </form>
    """

# =========================
# 🔴 SELL ORDER
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

        match_orders()
        return redirect('/')

    return """
    <h2>Sell Order</h2>
    <form method='post'>
        <input name='amount'><br><br>
        <input name='price'><br><br>
        <button>Submit Sell</button>
    </form>
    """

# =========================
# 🔥 INIT DB
# =========================
with app.app_context():
    db.create_all()

# =========================
# ▶ RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
