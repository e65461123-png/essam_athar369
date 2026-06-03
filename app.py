from flask import Flask, render_template

# هنا نخبر Flask أن يبحث عن الملفات في المجلد الحالي مباشرة
app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
