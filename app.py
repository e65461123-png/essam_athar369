from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secure-system'

db = SQLAlchemy(app)

# =====================
# USER MODEL
# =====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(20), default="user")

# =====================
# CHANGE PASSWORD (ADMIN ONLY)
# =====================
@app.route('/admin/change-password', methods=['POST'])
def change_password():

    if "role" not in session or session["role"] != "admin":
        return jsonify({"status": "denied"})

    data = request.json

    admin = User.query.filter_by(username=session["user"]).first()

    admin.password = generate_password_hash(data["new_password"])

    db.session.commit()

    return jsonify({"status": "password updated"})

# =====================
# ADMIN LOGIN
# =====================
@app.route('/login', methods=['POST'])
def login():

    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password, data["password"]):

        session["user"] = user.username
        session["role"] = user.role

        return jsonify({
            "status": "ok",
            "role": user.role
        })

    return jsonify({"status": "fail"})

# =====================
# ADMIN ROOM
# =====================
@app.route('/admin')
def admin_room():

    if "role" not in session or session["role"] != "admin":
        return "ACCESS DENIED"

    return jsonify({
        "room": "CONTROL CENTER",
        "tools": [
            "view users",
            "view orders",
            "change password",
            "system logs"
        ]
    })

# =====================
# INIT ADMIN
# =====================
with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username="Essam").first()

    if not admin:
        admin = User(
            username="Essam",
            password=generate_password_hash("SET_FIRST_PASSWORD"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
