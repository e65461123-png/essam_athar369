from flask import Blueprint, render_template, request, session, redirect, url_for
from app import db, User, Wallet, Transaction
from werkzeug.security import generate_password_hash, check_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    wallet = Wallet.query.get(session['user_id'])
    transactions = Transaction.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, wallet=wallet, transactions=transactions)

@main_bp.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session: return redirect(url_for('main.login'))
    amount = float(request.form.get('amount', 0))
    wallet = Wallet.query.get(session['user_id'])
    if wallet:
        wallet.balance_usd += amount
        new_trans = Transaction(user_id=session['user_id'], amount=amount)
        db.session.add(new_trans)
        db.session.commit()
    return redirect(url_for('main.dashboard'))

# ... (أضف دوال الـ register والـ login والـ logout هنا كما كانت سابقاً)
