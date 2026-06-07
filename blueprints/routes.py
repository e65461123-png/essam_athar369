from flask import Blueprint, render_template, request
from app import db, User
from werkzeug.security import generate_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "يجب إدخال اسم المستخدم وكلمة المرور"

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return "تم إنشاء الحساب بنجاح!"
    
    return render_template('register.html')
