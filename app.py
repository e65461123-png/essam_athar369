# في ملف app.py أو admin.py
from flask import Flask, render_template, request, redirect, session

# فرضاً أنك قمت بتعريف المسؤول مسبقاً في قاعدة البيانات
@app.route('/admin/dashboard')
def admin_dashboard():
    # تحقق من صلاحية الدخول (يجب أن يكون المسؤول هو من يدخل)
    if not session.get('is_admin'):
        return "غير مصرح لك بالدخول", 403
    
    # جلب البيانات من جداول قاعدة البيانات التي صممتها (Users, Wallets, Audit Logs)
    users = db.execute("SELECT * FROM users")
    logs = db.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 20")
    
    return render_template('admin_dashboard.html', users=users, logs=logs)

@app.route('/admin/update_balance', methods=['POST'])
def update_balance():
    # كود لتعديل رصيد أي مستخدم يدوياً في حال حدوث إيداع كاش مثلاً
    user_id = request.form.get('user_id')
    new_amount = request.form.get('amount')
    db.execute("UPDATE wallets SET balance = ? WHERE user_id = ?", new_amount, user_id)
    return redirect('/admin/dashboard')
