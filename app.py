from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# تعريف جدول المستخدمين
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# إنشاء قاعدة البيانات (يتم تنفيذها مرة واحدة)
with app.app_context():
    db.create_all()

# --- الصفحات ---
@app.route('/')
def home():
    return "مرحباً بك! <a href='/login'>تسجيل الدخول</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن المستخدم في قاعدة البيانات
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            return f"تم تسجيل دخولك بنجاح يا {username}!"
        else:
            return "خطأ: اسم المستخدم أو كلمة المرور غير صحيحة."
            
    return render_template_string("""
        <form method="POST">
            <input type="text" name="username" placeholder="اسم المستخدم" required><br>
            <input type="password" name="password" placeholder="كلمة المرور" required><br>
            <button type="submit">دخول</button>
        </form>
    """)

if __name__ == '__main__':
    app.run(debug=True)
