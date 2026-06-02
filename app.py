from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # يبحث Flask تلقائياً داخل مجلد 'templates' عن هذا الملف
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
