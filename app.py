from flask import Flask, render_template
import os

# نحدد المجلد الحالي كمسار رئيسي للبحث
app = Flask(__name__, template_folder=os.getcwd())

@app.route('/')
def home():
    # سيبحث الآن مباشرة في المجلد الرئيسي بدون الحاجة لمجلد templates
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
