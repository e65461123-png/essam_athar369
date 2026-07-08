from flask import Flask, render_template

app = Flask(__name__, template_folder="app/templates")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return '''
    <h1>هذا عنوان رئيسي - صفحة عن</h1>
    <p>هذه فقرة نصية توضح محتوى صفحة عن.</p>
    <a href="/">العودة للرئيسية</a>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
