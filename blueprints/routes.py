from flask import Blueprint, render_template, request, redirect, url_for, session
import sys
import os

# هذا السطر يخبر بايثون أن يبحث في المجلد الرئيسي للمشروع 
# مهما كان الملف الذي يحاول الاستيراد منه
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main_bp.route('/dashboard')
def dashboard():
    # هنا قمنا بالاستيراد بعد إضافة المسار الرئيسي
    from models.models import User, Wallet
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    wallet = Wallet.query.get(session['user_id'])
    return render_template('dashboard.html', user=user, wallet=wallet)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('main.dashboard'))
    return render_template('register.html')

@main_bp.route('/login')
def login():
    return "صفحة تسجيل الدخول"
