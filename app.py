from flask import Flask, request, jsonify

app = Flask(__name__)

# =====================
# HOME PAGE
# =====================
@app.route("/")
def home():
    return """
    <h1>📈 Exchange System</h1>
    <p>System Running 🚀</p>

    <h3>API Endpoints:</h3>
    <ul>
        <li>POST /register</li>
        <li>POST /login</li>
    </ul>
    """

# =====================
# SIMPLE STORAGE
# =====================
users = {}

# =====================
# REGISTER
# =====================
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"status": "error", "msg": "user exists"})

    users[username] = password

    return jsonify({"status": "success", "msg": "registered"})

# =====================
# LOGIN
# =====================
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        return jsonify({"status": "success", "msg": "logged in"})

    return jsonify({"status": "error", "msg": "invalid credentials"})

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
