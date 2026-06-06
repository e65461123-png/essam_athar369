from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ATHEER 369</title>
</head>
<body style="font-family: Arial; text-align:center; margin-top:50px;">
    <h1>🚀 مرحباً بك في المحفظة الرقمية</h1>
    <p>السيرفر يعمل بنجاح</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/health")
def health():
    return {"status": "ok", "message": "running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
