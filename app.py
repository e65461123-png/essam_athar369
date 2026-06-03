from flask import Flask, render_template_string, request, redirect, session, url_for
import smtplib # لربط زر المراسلة بالإيميل

app = Flask(__name__)
app.secret_key = "ATHEER_369_NUCLEAR_CORE"

# محاكاة قاعدة بيانات الخزنة
vault = {"total_invested": 0, "my_commission": 0}

STYLE = """
<style>
    body { background: #000; color: #0f0; font-family: 'Courier New', monospace; margin: 0; }
    .card { border: 1px solid #0f0; padding: 20px; width: 350px; margin: 20px auto; text-align: center; box-shadow: 0 0 15px #0f0; }
    button { width: 100%; padding: 10px; background: #0f0; color: #000; border: none; font-weight: bold; cursor: pointer; margin-top: 10px; }
    .ticker { background: #111; padding: 10px; color: #0f0; border-bottom: 1px solid #0f0; overflow: hidden; white-space: nowrap; }
    .footer { font-size: 0.7em; margin-top: 20px; color: #555; }
</style>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("username") == "Essam369" and request.form.get("password") == "369369":
            session["logged_in"] = True
            return redirect(url_for('dashboard'))
    return render_template_string(STYLE + "<body><div class='card'><h1>LOGIN</h1><form method='post'><input name='username' placeholder='USER'><input name='password' type='password' placeholder='PASS'><button>دخول القيادة</button></form></div></body>")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"): return redirect(url_for('home'))
    
    if request.method == "POST":
        if 'invest' in request.form: # منطق الخزنة
            amount = float(request.form.get("amount", 0))
            vault["my_commission"] += (amount * 0.10) # خصم 10% للخزنة
            vault["total_invested"] += amount
        return redirect(url_for('dashboard'))

    return render_template_string(f"""
    {STYLE}
    <body>
        <div class='ticker'>الذهب: $2350 | البيتكوين: $68000 | USD: 1.00 | ATHEER AI: نشط...</div>
        <div class='card'>
            <h2>غرفة العمليات</h2>
            <p>الخزنة (10%): ${vault['my_commission']}</p>
            <form method='post'>
                <input name='amount' placeholder='قيمة الاستثمار'>
                <button name='invest'>تفعيل تدفق مالي</button>
            </form>
            <br>
            <a href="mailto:your_email@gmail.com"><button style='background: #00f; color: #fff;'>مراسلة غرفة القيادة (GMAIL)</button></a>
            <br><br>
            <a href="/logout" style='color:red;'>تسجيل خروج</a>
            <div class='footer'>© 2026 ATHEER 369 | جميع الحقوق محفوظة</div>
        </div>
    </body>
    """)

@app.route("/logout")
def logout(): session.clear(); return redirect(url_for('home'))

if __name__ == "__main__": app.run()
