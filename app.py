from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>المحفظة الرقمية</title>
    <style>
        body { font-family: Arial; background:#111; color:#fff; text-align:center; }
        .box { margin-top:100px; padding:20px; background:#222; display:inline-block; border-radius:10px; }
    </style>
</head>
<body>

    <div class="box">
        <h2>عصام الكومي</h2>
        <p>رصيد المحفظة: USD {{ balance }}</p>
    </div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, balance="369.00")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
