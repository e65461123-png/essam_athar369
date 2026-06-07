from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# =====================
# DATABASE
# =====================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exchange.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =====================
# ORDERS MODEL
# =====================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    side = db.Column(db.String(10))  # buy / sell
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    filled = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default="open")

# =====================
# TRADES LOG
# =====================
class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buy_user = db.Column(db.String(80))
    sell_user = db.Column(db.String(80))
    price = db.Column(db.Float)
    amount = db.Column(db.Float)

# =====================
# MATCH ENGINE
# =====================
def match_orders():

    buys = Order.query.filter_by(side="buy", status="open").order_by(Order.price.desc()).all()
    sells = Order.query.filter_by(side="sell", status="open").order_by(Order.price.asc()).all()

    for b in buys:
        for s in sells:

            if b.price >= s.price and b.status == "open" and s.status == "open":

                amount = min(b.amount - b.filled, s.amount - s.filled)

                if amount <= 0:
                    continue

                b.filled += amount
                s.filled += amount

                if b.filled >= b.amount:
                    b.status = "filled"
                if s.filled >= s.amount:
                    s.status = "filled"

                trade = Trade(
                    buy_user=b.user,
                    sell_user=s.user,
                    price=s.price,
                    amount=amount
                )

                db.session.add(trade)
                db.session.commit()

# =====================
# PLACE ORDER
# =====================
@app.route("/order", methods=["POST"])
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

    # 🔥 تشغيل المطابقة فورًا
    match_orders()

    return jsonify({"status": "order placed", "matched": True})

# =====================
# ORDER BOOK
# =====================
@app.route("/book")
def book():

    buys = Order.query.filter_by(side="buy", status="open").all()
    sells = Order.query.filter_by(side="sell", status="open").all()

    return jsonify({
        "buy": [{"user": o.user, "amount": o.amount - o.filled, "price": o.price} for o in buys],
        "sell": [{"user": o.user, "amount": o.amount - o.filled, "price": o.price} for o in sells]
    })

# =====================
# TRADES
# =====================
@app.route("/trades")
def trades():

    data = Trade.query.order_by(Trade.id.desc()).limit(20).all()

    return jsonify([
        {
            "buy": t.buy_user,
            "sell": t.sell_user,
            "price": t.price,
            "amount": t.amount
        }
        for t in data
    ])

# =====================
# INIT DB
# =====================
with app.app_context():
    db.create_all()

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
