from flask import Flask, request, redirect, url_for, session, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-change'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# =========================
# 📊 DATABASE
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")
    balance = db.Column(db.Float, default=100.0)

# =========================
# 🏠 HOME
# =========================
@app.route('/')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return f"""
        <h2>👋 Welcome {user.username}</h2>
        <p>💰 Balance: {user.balance}$</p>
        <a href='/dashboard'>Dashboard</a><br>
        <a href='/logout'>Logout</a>
        """
    return """
    <h2>🏠 Home</h2>
    <a href='/login'>Login</a> |
    <a href='/register'>Register</a>
    """

# =========================
# 🆕 REGISTER
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "❌ Username already exists"

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template_string("""
    <h2>🆕 Register</h2>
    <form method="post">
        <input name="username" placeholder="Username"><br>
        <input name="password" type="password" placeholder="Password"><br>
        <button type="submit">Register</button>
    </form>
    """)

# =========================
# 🔐 LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect('/dashboard')

        return "❌ Invalid credentials"

    return render_template_string("""
    <h2>🔐 Login</h2>
    <form method="post">
        <input name="username" placeholder="Username"><br>
        <input name="password" type="password" placeholder="Password"><br>
        <button type="submit">Login</button>
    </form>
    """)

# =========================
# 📊 DASHBOARD
# =========================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])

    admin_panel = ""
    if user.role == "admin":
        admin_panel = "<a href='/admin'>⚙ Admin Panel</a><br>"

    return f"""
    <h2>📊 Dashboard</h2>
    <p>👤 User: {user.username}</p>
    <p>💰 Balance: {user.balance}$</p>

    {admin_panel}

    <a href='/add_money'>➕ Add Money</a><br>
    <a href='/logout'>Logout</a>
    """

# =========================
# 💰 ADD MONEY (Wallet)
# =========================
@app.route('/add_money')
def add_money():
    if 'user_id' not in session:
        return redirect('/login')

    user = User.query.get(session['user_id'])
    user.balance += 50
    db.session.commit()

    return redirect('/dashboard')

# =========================
# ⚙ ADMIN PANEL
# =========================
@app.route('/admin')
def admin():
    if 'role' not in session or session['role'] != 'admin':
        return "⛔ Not allowed"

    users = User.query.all()

    users_list = "".join(
        f"<li>{u.username} - {u.balance}$ - {u.role}</li>" for u in users
    )

    return f"""
    <h2>⚙ Admin Panel</h2>
    <ul>{users_list}</ul>
    <a href='/dashboard'>Back</a>
    """

# =========================
# 🚪 LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# =========================
# 🔥 INIT DB + ADMIN SEED
# =========================
with app.app_context():
    db.create_all()

    # إنشاء admin تلقائي لو مش موجود
    if not User.query.filter_by(username="admin").first():
        admin_pass = bcrypt.generate_password_hash("admin123").decode('utf-8')
        admin_user = User(username="admin", password=admin_pass, role="admin", balance=9999)
        db.session.add(admin_user)
        db.session.commit()

# =========================
# ▶ RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
