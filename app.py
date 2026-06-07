from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# USERS
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

# =========================
# ORDERS
# =========================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80))
    side = db.Column(db.String(10))
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    status = db.Column(db.String(20), default="open")

# =========================
# HOME (IMPORTANT)
# =========================
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "PRO EXCHANGE WORKING",
        "endpoints": ["/register", "/order", "/book"]
    })

# =========================
# REGISTER (MERGED)
# =========================
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    u = User(username=data["username"])
    db.session.add(u)
    db.session.commit()

    return jsonify({"msg": "user created"})

# =========================
# PLACE ORDER
# =========================
@app.route('/order', methods=['POST'])
def order():
    data = request.json

    o = Order(
        user=data["user"],
        side=data["side"],
        amount=data["amount"],
        price=data["price"]
    )

    db.session.add(o)
    db.session.commit()

    return jsonify({"msg": "order placed"})

# =========================
# ORDER BOOK
# =========================
@app.route('/book')
def book():

    buys = Order.query.filter_by(side="buy").all()
    sells = Order.query.filter_by(side="sell").all()

    return jsonify({
        "buy": [{"price": o.price, "amount": o.amount} for o in buys],
        "sell": [{"price": o.price, "amount": o.amount} for o in sells]
    })

# =========================
# INIT DB
# =========================
with app.app_context():
    db.create_all()

# =========================
# RUN (RENDER SAFE)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
