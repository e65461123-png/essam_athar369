from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="utf-8">
<title>ATHEER 369</title>
<style>
body{
    background:#0b1220;
    color:white;
    font-family:Arial;
    margin:0;
}
.header{
    background:#111827;
    padding:20px;
    text-align:center;
}
.card{
    background:#1f2937;
    margin:20px;
    padding:20px;
    border-radius:10px;
}
button{
    padding:10px 20px;
    border:none;
    border-radius:8px;
    cursor:pointer;
}
.buy{background:#10b981;color:white;}
.sell{background:#ef4444;color:white;}
</style>
</head>
<body>

<div class="header">
<h1>ATHEER 369</h1>
</div>

<div class="card">
<h2>السوق المباشر</h2>
<p>الرصيد: $1000</p>
<button class="buy">شراء</button>
<button class="sell">بيع</button>
</div>

<div class="card">
<h2>لوحة المستثمرين</h2>
<p>مرحباً بك في منصة ATHEER 369</p>
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
