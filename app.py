from flask import Flask, render_template
import os

# إعداد Flask للبحث في المجلد الحالي مباشرة
app = Flask(__name__, template_folder=os.path.abspath(os.path.dirname(__file__)))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
