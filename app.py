@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>EXCHANGE LIVE</title>
    </head>
    <body style="background:#0f172a;color:white;text-align:center;font-family:Arial">

        <h1>📈 EXCHANGE LIVE</h1>
        <p>Platform Running 🚀</p>

        <button onclick="location.href='/book'">📊 Orders</button>

    </body>
    </html>
    """
