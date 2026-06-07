@app.route("/")
def home():
    return """
    <h1>📈 Exchange System</h1>
    <p>Use API:</p>
    <ul>
        <li>/register (POST)</li>
        <li>/login (POST)</li>
    </ul>
    """
