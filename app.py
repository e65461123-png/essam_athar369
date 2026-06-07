from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# =====================
# DATABASE
# =====================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =====================
# USER MODEL
# =====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# =====================
# HOME PAGE
# =====================
@app.route("/")
def home():
    return """
    <h1>📈 Welcome to Exchange</h1>
    <p>Use /register to create account</p>
    """

# =====================
# REGISTER
# =====================
@app.route("/register", methods=["POST"])
def register():

    data = request.json

    if not data.get("username") or not data.get("password"):
        return jsonify({"status": "error", "msg": "missing data"})

    # check if user exists
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"status": "error", "msg": "user exists"})

    user = User(
        username=data["username"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"status": "success", "msg": "user created"})

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
        return jsonify({"status": "success", "msg": "logged in"})

    return jsonify({"status": "error", "msg": "invalid credentials"})

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
