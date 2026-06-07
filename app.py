@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>EXCHANGE LIVE</title>
    </head>
    <body style="font-family:Arial;text-align:center;background:#111;color:white;">
        <h1>📈 EXCHANGE LIVE</h1>
        <p>Platform Online ✅</p>

        <a href="/book">Order Book</a>
    </body>
    </html>
    """
