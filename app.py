@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Live Exchange</title>
        <style>
            body { background:#0f172a; color:white; font-family:Arial; text-align:center; }
            a { color:#22c55e; font-size:20px; display:block; margin:10px; }
        </style>
    </head>

    <body>
        <h1>📈 LIVE EXCHANGE SYSTEM</h1>

        <a href="/book">📊 Order Book</a>
        <a href="/trades">💰 Trades</a>

        <p>System is running 🚀</p>
    </body>
    </html>
    """
