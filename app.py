from flask import Flask, render_template

app = Flask(__name__)

# المسار الرئيسي للموقع
@app.route('/')
@app.route('/dashboard')
def user_dashboard():
    # مؤقتاً هنخليه يفتح ملف dashboard.html الشغال عندك عشان الموقع يقوم
    user_data = {
        'username': 'عصام الكومي',
        'balance': '1,250.00'
    }
    return render_template('dashboard.html', data=user_data)

# مسار لوحة التحكم
@app.route('/admin/dashboard')
def admin_dashboard():
    admin_data = {
        'username': 'admin',
        'balance': '369.0'
    }
    return render_template('dashboard.html', data=admin_data)

if __name__ == '__main__':
    app.run(debug=True)
