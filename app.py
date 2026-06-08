from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # هذا الكود سيجبر السيرفر على إعادة تحميل index.html دائماً
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
