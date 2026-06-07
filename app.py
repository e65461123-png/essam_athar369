from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultra-exchange-core'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exchange.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# 👤 USERS
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    balance = db.Column(db.Float, default=1000.0)

# =========================
# 📊 ORDERS (REAL ORDER BOOK)
# =========================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    side = db.Column(db.String(4))  # buy / sell
    price = db.Column(db.Float)
    amount = db.Column(db.Float)
    filled = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default="open")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# 💰 TRADES (EXECUTIONS)
# =========================
class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buy_user = db.Column(db.String(80))
    sell_user = db.Column(db.String(80))
    price = db.Column(db.Float)
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# ⚡ MATCHING ENGINE (REAL CORE)
# =========================
def match_engine():

    buys = Order.query.filter_by(side="buy", status="open").order_by(Order.price.desc(), Order.timestamp.asc()).all()
    sells = Order.query.filter_by(side="sell", status="open").order_by(Order.price.asc(), Order.timestamp.asc()).all()

    for buy in buys:
        for sell in sells:

            if buy.price >= sell.price and buy.status == "open" and sell.status == "open":

                trade_amount = min(buy.amount - buy.filled, sell.amount - sell.filled)
                trade_price = sell.price

                # update fills
                buy.filled += trade_amount
                sell.filled += trade_amount

                # mark status
                if buy.filled >= buy.amount:
                    buy.status = "filled"
                if sell.filled >= sell.amount:
                    sell.status = "filled"

                # save trade
                trade = Trade(
                    buy_user=buy.user,
                    sell_user=sell.user,
                    price=trade_price,
                    amount=trade_amount
                )
                db.session.add(trade)

                db.session.commit()

# =========================
# 🆕 REGISTER
# =========================
@app.route('/register', methods=['POST'])
def register():

    data = request.json

    user = User(
        username=data["username"],
        password=generate_password_hash(data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"status": "user created"})

# =========================
# 🔐 LOGIN
# =========================
@app.route('/login', methods=['POST'])
def login():

    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password, data["password"]):
        return jsonify({"status": "ok"})

    return jsonify({"status": "fail"})

# =========================
# 📥 PLACE ORDER (REAL API)
# =========================
@app.route('/order', methods=['POST'])
def place_order():

    data = request.json

    order = Order(
        user=data["user"],
        side=data["side"],
        price=float(data["price"]),
        amount=float(data["amount"])
    )

    db.session.add(order)
    db.session.commit()

    match_engine()

    return jsonify({"status": "order placed"})

# =========================
# 📊 ORDER BOOK
# =========================
@app.route('/book')
def book():

    buys = Order.query.filter_by(side="buy", status="open").all()
    sells = Order.query.filter_by(side="sell", status="open").all()

    return jsonify({
        "buy": [
            {"user": o.user, "price": o.price, "amount": o.amount - o.filled}
            for o in buys
        ],
        "sell": [
            {"user": o.user, "price": o.price, "amount": o.amount - o.filled}
            for o in sells
        ]
    })

# =========================
# 💰 USERS WALLET VIEW
# =========================
@app.route('/wallet/<username>')
def wallet(username):

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "not found"})

    return jsonify({
        "user": user.username,
        "balance": user.balance
    })

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
