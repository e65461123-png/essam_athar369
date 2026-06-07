@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>EXCHANGE LIVE</title>
        <style>
            body{
                background:#0f172a;
                color:white;
                font-family:Arial;
                text-align:center;
                padding-top:50px;
            }
            .card{
                background:#1e293b;
                width:400px;
                margin:auto;
                padding:20px;
                border-radius:15px;
            }
            a{
                display:block;
                margin:10px;
                color:#22c55e;
                text-decoration:none;
                font-size:20px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>📈 EXCHANGE LIVE</h1>
            <p>Platform Online ✅</p>

            <a href="/register">🔐 Register</a>
            <a href="/login">👤 Login</a>
            <a href="/book">📊 Order Book</a>
        </div>
    </body>
    </html>
    """
