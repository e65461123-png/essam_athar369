from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'AETHER_369_SECRET_KEY'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    # هنا لا نستخدم أي قاعدة بيانات حتى نضمن عدم حدوث خطأ
    # سنعرض صفحة لوحة التحكم مباشرة
    return render_template('admin_dashboard.html', users=[], logs=[])

@app.route('/admin/update_balance', methods=['POST'])
def update_balance():
    # مجرد إعادة توجيه للوحة حتى نربط قاعدة البيانات لاحقاً
    return redirect('/admin/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
