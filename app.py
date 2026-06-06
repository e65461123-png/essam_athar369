from flask import Flask, render_template

app = Flask(__name__)

# الصفحة الرئيسية - هتعرض لوحة التحكم فوراً بدون تعقيد
@app.route('/')
@app.route('/admin/dashboard')
def admin_dashboard():
    # البيانات اللي هتروح للـ HTML بشكل مباشر وآمن
    admin_data = {
        'username': 'admin',
        'balance': '369.0'
    }
    return render_template('dashboard.html', data=admin_data)

if __name__ == '__main__':
    app.run(debug=True)
