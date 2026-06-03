from flask import Flask, render_template

# السطر الذي سألت عنه، يدمج البحث في المجلد الحالي
app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
