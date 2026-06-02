from flask import Flask, render_template

app = Flask(__name__)

# هذا المسار يفتح صفحة الدخول مباشرة عند زيارة الموقع
@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
