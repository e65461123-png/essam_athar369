from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# قاعدة بيانات SQLite بسيطة
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =====================
# USERS
# =====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    balance = db.Column(db.Float, default=1000)

# =====================
# ORDERS
# =====================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    type = db.Column(db.String(10))  # BUY / SELL
    amount = db.Column(db.Float)
    price = db.Column(db.Float)

# إنشاء الجداول
with app.app_context():
    db.create_all()

# =====================
# HOME
# =====================
@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "MVP EXCHANGE READY"
    })

# =====================
# REGISTER
# =====================
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"status": "error", "msg": "user exists"})

    user = User(
        username=data["username"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"status": "success", "msg": "registered"})

# =====================
# LOGIN
# =====================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(
        username=data["username"],
        password=data["password"]
    ).first()

    if user:
        return jsonify({
            "status": "success",
            "balance": user.balance
        })

    return jsonify({"status": "error", "msg": "invalid credentials"})

# =====================
# PLACE ORDER
# =====================
@app.route("/order", methods=["POST"])
def order():
    data = request.json

    new_order = Order(
        username=data["username"],
        type=data["type"],
        amount=data["amount"],
        price=data["price"]
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({"status": "success", "msg": "order placed"})

# =====================
# BOOK
# =====================
@app.route("/book")
def book():
    orders = Order.query.all()

    return jsonify([{
        "user": o.username,
        "type": o.type,
        "amount": o.amount,
        "price": o.price
    } for o in orders])

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
