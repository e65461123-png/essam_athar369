from flask import Flask, render_template

app = Flask(__name__)

# المسار الرئيسي للموقع (أول ما تفتح الرابط الأساسي)
@app.route('/')
def home():
    # هنمرر البيانات مباشرة لملف الـ HTML
    admin_data = {
        'username': 'admin',
        'balance': '369.0'
    }
    return render_template('dashboard.html', data=admin_data)

# مسار احتياطي لو كتبت /admin/dashboard في الرابط
@app.route('/admin/dashboard')
def admin_dashboard():
    admin_data = {
        'username': 'admin',
        'balance': '369.0'
    }
    return render_template('dashboard.html', data=admin_data)

if __name__ == '__main__':
    app.run(debug=True)
