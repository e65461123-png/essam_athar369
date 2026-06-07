from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# بيانات مؤقتة
users = {}
orders = []

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>EXCHANGE LIVE</title></head>
    <body style="background:#0f172a; color:white; font-family:Arial; text-align:center; padding-top:40px;">
        <div style="background:#1e293b; width:420px; margin:auto; padding:20px; border-radius:12px;">
            <h1>📈 EXCHANGE LIVE</h1>
            <p>System Running 🚀</p>
            <button onclick="location.href='/dashboard'" style="padding:10px; width:80%; cursor:pointer;">📊 View Orders</button>
        </div>
    </body>
    </html>
    """

# مسار عرض صفحة dashboard.html
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username in users: return jsonify({"status":"error","msg":"user exists"})
    users[username] = password
    return jsonify({"status":"success","msg":"registered"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if users.get(username) == password: return jsonify({"status":"success","msg":"logged in"})
    return jsonify({"status":"error","msg":"invalid credentials"})

@app.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    orders.append({"user": data.get("user"), "type": data.get("type"), "amount": data.get("amount"), "price": data.get("price")})
    return jsonify({"status":"success","msg":"order placed"})

@app.route("/book")
def book():
    return jsonify(orders)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
