from flask import Blueprint, render_template, request, redirect, url_for, session

# تعريف الـ Blueprint
main_bp = Blueprint('main', __name__)

# استيراد محلي لتجنب مشاكل الـ Import
def get_user_model():
    from models.models import User, Wallet
    return User, Wallet

@main_bp.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main_bp.route('/dashboard')
def dashboard():
    User, Wallet = get_user_model()
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    wallet = Wallet.query.get(session['user_id'])
    return render_template('dashboard.html', user=user, wallet=wallet)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # أضف هنا منطق التسجيل الخاص بك
        return redirect(url_for('main.dashboard'))
    return render_template('register.html')

@main_bp.route('/login')
def login():
    return "صفحة تسجيل الدخول - قم ببرمجتها هنا"
