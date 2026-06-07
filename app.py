from flask import Flask, jsonify, request

app = Flask(__name__)

orders = []

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "EXCHANGE LIVE"
    })

@app.route("/order", methods=["POST"])
def order():
    data = request.json

    orders.append({
        "user": data.get("user"),
        "side": data.get("side"),
        "amount": data.get("amount"),
        "price": data.get("price")
    })

    return jsonify({"status": "order added"})

@app.route("/book")
def book():
    return jsonify({
        "buy": [o for o in orders if o["side"] == "buy"],
        "sell": [o for o in orders if o["side"] == "sell"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
