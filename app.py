from flask import Flask, render_template

app = Flask(__name__)

# هذا الكود يجبر الموقع على فتح صفحة الدخول فوراً
@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
