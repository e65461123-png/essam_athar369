from flask import Flask, request, jsonify

app = Flask(__name__)

users = []
orders = []

@app.route("/")
def home():
    return """
    <h1>📈 EXCHANGE LIVE</h1>
    <p>Platform Online ✅</p>
    """

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    users.append({
        "username": data.get("username"),
        "password": data.get("password")
    })

    return jsonify({
        "status": "success",
        "message": "تم إنشاء الحساب"
    })

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    for user in users:
        if (
            user["username"] == data.get("username")
            and user["password"] == data.get("password")
        ):
            return jsonify({
                "status": "success",
                "message": "تم تسجيل الدخول"
            })

    return jsonify({
        "status": "error",
        "message": "بيانات غير صحيحة"
    }), 401

@app.route("/place_buy_order", methods=["POST"])
def place_buy_order():
    data = request.get_json()

    order = {
        "amount": data.get("amount"),
        "price": data.get("price"),
        "type": "BUY"
    }

    orders.append(order)

    return jsonify({
        "status": "success",
        "message": "تم إرسال أمر الشراء",
        "order": order
    })

@app.route("/book")
def book():
    return jsonify(orders)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
