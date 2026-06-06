@app.route("/admin")
def admin():
    if session.get("user") != "admin":
        return "Access Denied ❌"

    users_count = 1  # تقدر تربطها بقاعدة البيانات لاحقًا

    return f"""
    <h1>ADMIN CONTROL ROOM</h1>
    <p>System Status: RUNNING 🟢</p>
    <p>Total Users: {users_count}</p>
    <p>Current Admin: {session.get('user')}</p>
    """
