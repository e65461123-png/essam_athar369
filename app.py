from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # ضع هنا مفتاحاً سرياً خاصاً بك

# مسار الصفحة الرئيسية (صفحة الدخول)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        
        # منطق التحقق من البيانات
        if user == "admin" and password == "12345":
            session['logged_in'] = True
            session['user'] = user
            return redirect(url_for('dashboard'))
        else:
            return "خطأ: بيانات الدخول غير صحيحة"
    return render_template('login.html')

# لوحة تحكم المستخدم
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# لوحة تحكم المسؤول (للصلاحيات المتقدمة)
@app.route('/admin')
def admin():
    if session.get('user') != 'admin':
        return "تم الرفض: غير مسموح لك بالدخول"
    return render_template('admin.html')

if __name__ == '__main__':
    app.run()
