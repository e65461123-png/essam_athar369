from flask import Flask, render_template_string, request, session, redirect, url_for, g
import random

app = Flask(__name__)
app.secret_key = "ATHEER_369_FINAL_PRO"

# بيانات المحرك المالي واللغات
DATA = {
    'ar': {'title': 'منصة ATHEER 369 للوساطة', 'vault': 'الخزنة:', 'invest': 'تفعيل', 'ticker': 'السوق'},
    'en': {'title': 'ATHEER 369 Brokerage', 'vault': 'Vault:', 'invest': 'Activate', 'ticker': 'Market'},
    'es': {'title': 'ATHEER 369 Brokerage', 'vault': 'Bóveda:', 'invest': 'Activar', 'ticker': 'Mercado'}
}

@app.before_request
def setup(): g.lang = session.get('lang', 'ar')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form.get("amount", 0))
        session['vault'] = session.get('vault', 0) + (amount * 0.10)
    
    # محاكاة أسعار حية
    prices = f"GOLD: ${2300 + random.random()} | BTC: ${68000 + random.randint(1,100)}"
    
    template = """
    <body style="background:#000; color:#0f0; font-family:monospace; text-align:center;">
        <div style="background:#111; padding:10px; border-bottom:1px solid #0f0;">{{ DATA[g.lang]['ticker'] }}: {{ prices }}</div>
        <nav style="padding:10px;"><a href="/lang/ar">AR</a> | <a href="/lang/en">EN</a> | <a href="/lang/es">ES</a></nav>
        <h1>{{ DATA[g.lang]['title'] }}</h1>
        <div style="border:1px solid #0f0; width:300px; margin:20px auto; padding:20px;">
            <p>{{ DATA[g.lang]['vault'] }} ${{ "%.2f"|format(session.get('vault', 0)) }}</p>
            <form method="post"><input name="amount" type="number" placeholder="Amount" style="background:#000; color:#0f0; border:1px solid #0f0;"><br><br>
            <button style="background:#0f0; border:none; padding:10px 20px;">{{ DATA[g.lang]['invest'] }}</button></form>
        </div>
    </body>
    """
    return render_template_string(template, DATA=DATA, prices=prices)

@app.route("/lang/<l>")
def set_lang(l): session['lang'] = l; return redirect(url_for('index'))

if __name__ == "__main__": app.run()
