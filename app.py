@app.route("/order", methods=["POST"])
def order():

    data = request.json

    user = data["user"]
    side = data["side"]   # buy / sell
    amount = float(data["amount"])
    price = float(data["price"])

    # هنا بنسجل الأمر (مؤقتًا في memory)
    order = {
        "user": user,
        "side": side,
        "amount": amount,
        "price": price
    }

    if "orders" not in globals():
        global orders
        orders = []

    orders.append(order)

    return jsonify({
        "status": "order placed",
        "order": order
    })
