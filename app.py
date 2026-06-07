from flask import Flask, request, jsonify
from models import db, Order # افترضنا وجود ملف models يحتوي على كلاس Order

@app.route('/place_buy_order', methods=['POST'])
def place_buy_order():
    data = request.get_json()
    amount = data.get('amount')
    price = data.get('price')
    
    # التحقق من البيانات
    if not amount or not price:
        return jsonify({"status": "error", "message": "البيانات غير مكتملة"}), 400
    
    # إنشاء طلب جديد
    new_order = Order(amount=amount, price=price, type='BUY', status='PENDING')
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "تم إرسال أمر الشراء بنجاح"})
