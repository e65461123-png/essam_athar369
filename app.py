from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# واجهة المستخدم الاحترافية
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ATHEER 369 - منصة التداول</title>
    <style>
        body { background: #1a1a1a; color: white; font-family: sans-serif; text-align: center; padding: 50px; }
        .card { background: #2d2d2d; padding: 20px; border-radius: 15px; display: inline-block; width: 300px; }
        button { background: #f3ba2f; border: none; padding: 15px 30px; border-radius: 5px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h1>ATHEER 369</h1>
        <p>رصيدك الحالي: <span id="balance">1000.00</span> $</p>
        <button onclick="invest()">استثمار الآن</button>
    </div>
    <script>
        async function invest() {
            const res = await fetch('/api/invest', {method: 'POST'});
            const data = await res.json();
            document.getElementById('balance').innerText = data.new_balance;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/invest', methods=['POST'])
def invest():
    # هنا يتم ربط منطق الـ 61 بند في كل عملية
    return jsonify({"new_balance": 1050.00, "status": "SUCCESS"})

if __name__ == '__main__':
    app.run()
