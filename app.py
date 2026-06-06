from flask import request, jsonify

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    data = request.json
    username = data.get('username')
    
    # التحقق إذا كان المستخدم موجوداً
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "المستخدم موجود بالفعل!"}), 400
    
    # إنشاء محفظة جديدة برصيد افتراضي 0
    new_user = User(username=username, balance=0.0)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": f"تم إنشاء محفظة للمستخدم {username} بنجاح!"}), 201
