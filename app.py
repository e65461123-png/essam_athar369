@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>AETHER 369</title>
        <style>
            body{
                background:#0b0b0b;
                color:white;
                text-align:center;
                font-family:Arial;
                margin-top:50px;
            }

            .card{
                width:80%;
                margin:auto;
                padding:20px;
                border:1px solid #00ff99;
                border-radius:15px;
            }

            h1{
                color:#00ff99;
            }

            a{
                display:inline-block;
                margin:10px;
                padding:12px 20px;
                background:#00ff99;
                color:black;
                text-decoration:none;
                border-radius:8px;
                font-weight:bold;
            }

            a:hover{
                opacity:.8;
            }
        </style>
    </head>
    <body>

        <div class="card">

            <h1>🔥 AETHER 369</h1>

            <h2>👑 القائد: عصام الكومي</h2>

            <hr>

            <h3>مرحباً بك في المحفظة الرقمية</h3>

            <p>نظام إدارة المحافظ والأرصدة الرقمية</p>

            <a href="/initdb">تهيئة قاعدة البيانات</a>

            <a href="/balance/essam">عرض رصيد Essam</a>

        </div>

    </body>
    </html>
    """
