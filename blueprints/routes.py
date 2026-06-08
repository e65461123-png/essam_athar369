from flask import Blueprint, render_template, request, session, redirect, url_for
from extensions import db
# سنقوم باستيراد الموديلز داخل الدوال فقط لكسر الحلقة الدائرية
# لا تضع استيراد الموديلز هنا في الأعلى

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    from models.models import User, Wallet # استيراد محلي
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    wallet = Wallet.query.get(session['user_id'])
    return render_template('dashboard.html', user=user, wallet=wallet)

@main_bp.route('/deposit', methods=['POST'])
def deposit():
    from models.models import Wallet, AuditLog # استيراد محلي
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    amount = float(request.form.get('amount', 0))
    wallet = Wallet.query.get(session['user_id'])
    
    if wallet:
        wallet.balance_usd += amount
        new_trans = AuditLog(action=f"Deposit: {amount}")
        db.session.add(new_trans)
        db.session.commit()
        
    return redirect(url_for('main.dashboard'))
@main_bp.route('/')
def index():
    return redirect(url_for('main.dashboard'))
