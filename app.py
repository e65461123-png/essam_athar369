from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey' # اجعلها أي نص عشوائي

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # التحقق من الجلسة بدون التسبب في خطأ برمجيات
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
