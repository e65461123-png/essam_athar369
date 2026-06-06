from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'trade-app-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trade.db'
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

# =========================
# 📊 ORDER MODEL
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
# 🏠 DASHBOARD
# =========================
@app.route('/')
def home():

    orders = Order.query.all()

    buy_rows = ""
    sell_rows = ""

    for o in orders:
        row = f"<tr><td>{o.amount}</td><td>{o.price}</td></tr>"
        if o.type == "buy":
            buy_rows += row
        else:
            sell_rows += row

    return f"""
    <html>
    <head>
        <title>Trading Platform</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body class="bg-dark text-white text-center">

        <h1 class="mt-4">📈 Trading Platform</h1>
        <p>💰 Live Exchange System</p>

        <div class="mt-3">
            <a class="btn btn-success m-2" href="/buy">Buy</a>
            <a class="btn btn-danger m-2" href="/sell">Sell</a>
            <a class="btn btn-primary m-2" href="/orders">Orders</a>
        </div>

        <div class="container mt-4 row">

            <div class="col-md-6">
                <h3>🟢 Buy Orders</h3>
                <table class="table table-dark">
                    <tr><th>Amount</th><th>Price</th></tr>
                    {buy_rows}
                </table>
            </div>

            <div class="col-md-6">
                <h3>🔴 Sell Orders</h3>
                <table class="table table-dark">
                    <tr><th>Amount</th><th>Price</th></tr>
                    {sell_rows}
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

        return redirect('/')

    return """
    <form method='post'>
        <h2>Buy Order</h2>
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

        return redirect('/')

    return """
    <form method='post'>
        <h2>Sell Order</h2>
        <input name='amount'><br><br>
        <input name='price'><br><br>
        <button>Submit Sell</button>
    </form>
    """

# =========================
# 📊 ALL ORDERS PAGE
# =========================
@app.route('/orders')
def orders():
    data = Order.query.all()

    html = "<h2>📊 All Orders</h2>"

    for o in data:
        html += f"<p>{o.user} | {o.type} | {o.amount} | {o.price} | {o.status}</p>"

    html += "<br><a href='/'>Back</a>"
    return html

# =========================
# 🔥 INIT DATABASE
# =========================
with app.app_context():
    db.create_all()

# =========================
# ▶ RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
