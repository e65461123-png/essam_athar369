from flask import Flask, render_template

app = Flask(__name__)

# 1. لوحة تحكم المستخدم العادي (العميل) - المسار الرئيسي للموقع
@app.route('/')
@app.route('/dashboard')
def user_dashboard():
    # هنا البيانات الشاملة اللي واجهة المستخدم مستنياها عشان الأرقام تظهر
    user_data = {
        'username': 'عصام الكومي',
        'wallet_balance': '1,250.00',
        'btc_price': '68,230.00',  
        'gold_price': '2,340.00'
    }
    return render_template('user_dashboard.html', data=user_data)

# 2. لوحة تحكم الأدمن (المسؤول)
@app.route('/admin/dashboard')
def admin_dashboard():
    admin_data = {
        'username': 'admin',
        'balance': '369.0'
    }
    return render_template('dashboard.html', data=admin_data)

if __name__ == '__main__':
    app.run(debug=True)
