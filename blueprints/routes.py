@main_bp.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    amount = float(request.form.get('amount', 0))
    wallet = Wallet.query.get(session['user_id'])
    
    if wallet:
        wallet.balance_usd += amount
        db.session.commit()
    
    return redirect(url_for('main.dashboard'))
