from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'AETHER_369_SECRET_KEY'

# نجعل الصفحة الرئيسية هي admin_dashboard.html مؤقتاً 
# حتى لا يظهر خطأ 500 بسبب غياب index.html
@app.route('/')
def home():
    return render_template('admin_dashboard.html', users=[], logs=[])

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html', users=[], logs=[])

@app.route('/admin/update_balance', methods=['POST'])
def update_balance():
    return redirect('/admin/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
