@app.route("/")
def home():
    return """
    <html dir="rtl">
    <head>
    <title>AETHER 369</title>
    <style>
    body{
        background:#0f172a;
        color:white;
        font-family:Tahoma;
        text-align:center;
        padding-top:50px;
    }
    .card{
        width:350px;
        margin:auto;
        background:#1e293b;
        padding:20px;
        border-radius:15px;
    }
    a{
        display:block;
        margin:10px;
        padding:10px;
        background:#2563eb;
        color:white;
        text-decoration:none;
        border-radius:10px;
    }
    </style>
    </head>
    <body>
    <div class="card">
    <h1>AETHER 369</h1>
    <h3>القائد: عصام الكومي</h3>
    <p>رصيد المحفظة: USD 369.00</p>

    <a href="/login">تسجيل الدخول</a>
    <a href="/register">إنشاء حساب</a>
    </div>
    </body>
    </html>
    """
