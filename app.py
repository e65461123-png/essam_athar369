from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# الرصيد (مؤقتاً في الذاكرة حتى تربط قاعدة البيانات)
data = {"user": "admin", "balance": 369.0}

@app.route('/')
def home():
    return render_template('index.html', user=data["user"], balance=data["balance"])

@app.route('/update_balance', methods=['POST'])
def update_balance():
    amount = float(request.form.get('amount', 0))
    action = request.form.get('action')
    if action == 'deposit':
        data["balance"] += amount
    elif action == 'withdraw' and data["balance"] >= amount:
        data["balance"] -= amount
    return redirect('/')

if __name__ == '__main__':
    app.run()
