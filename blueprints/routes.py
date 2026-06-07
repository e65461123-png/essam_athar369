from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
# تأكد من استيراد db و User من ملف app.py (قد تحتاج لعمل import من __main__ أو هيكلة المشروع)
# إذا واجهت مشكلة في الاستيراد، أخبرني لنحلها معاً.

main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # تشفير كلمة المرور (هام جداً للأمان)
        hashed_pw = generate_password_hash(password, method='sha256')
        
        # إنشاء مستخدم جديد
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return "تم إنشاء الحساب بنجاح!"
    return render_template('register.html')
