from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "AETHER369_SECRET_KEY")

# =====================
# DATABASE FIX
# =====================
db_url = os.environ.get("DATABASE_URL", "sqlite:///aether369.db")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =====================
# MODEL
# =====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=1250.0)

# =====================
# INIT DATABASE + USERS
# =====================
def init_db():
    with app.app_context():
        db.create_all()

        # 👤 USER: Essam369
        user1 = User.query.filter_by(username="Essam369").first()
        if not user1:
            user1 = User(
                username="Essam369",
                password=generate_password_hash("369369"),
                balance=369.0
            )
            db.session.add(user1)

        # 👑 ADMIN
        admin = User.query.filter_by(username="admin").first()
        if not admin:
            admin = User(
                username="admin",
                password=generate_password_hash("1234"),
                balance=1250.0
            )
            db.session.add(admin)

        db.session.commit()

init_db()

# =====================
@app.route("/")
def home():
    return render_template("home.html")

# =====================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(username=username).first():
            return "❌ المستخدم موجود بالفعل"

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# =====================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.username
            return redirect("/dashboard")

        return "❌ بيانات الدخول غير صحيحة"

    return render_template("login.html")

# =====================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user = User.query.filter_by(username=session["user"]).first()

    if not user:
        session.clear()
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=user.username,
        balance=user.balance
    )

# =====================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
