from flask import Flask, render_template_string, request, session, redirect, url_for, g
import random

app = Flask(__name__)
app.secret_key = "ATHEER_369_FINAL_DEPLOY"

# إعدادات النظام
DATA = {
    'ar': {'title': 'منصة ATHEER 369', 'vault': 'الرصيد:', 'invest': 'تنفيذ', 'market': 'السوق المباشر'},
    'en': {'title': 'ATHEER 369 Portal', 'vault': 'Balance:', 'invest': 'Execute', 'market': 'Live Market'}
}

@app.before_request
def setup(): g.lang = session.get('lang', 'ar')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form.get("amount", 0))
        session['vault'] = session.get('vault', 0) + (amount * 0.10)
    
    ticker = f"GOLD: ${2300 + random.random():.2f} | BTC: ${68000 + random.randint(1,50)}"
    
    # كود CSS احترافي (السر في التصميم المالي)
    css = """
    <style>
        body { background: #0a0a0a; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; }
        .ticker { background: #1a1a1a; padding: 10px; color: #0f0; border-bottom: 2px solid #333; }
        .box { border: 1px solid #333; background: #111; width: 400px; margin: 50px auto; padding: 30px; border-radius: 10px; }
        input { background: #000; border: 1px solid #444; color: #fff; padding: 10px; width: 80%; margin: 10px 0; }
        button { background: #00ff41; border: none; padding: 10px 30px; cursor: pointer; color: #000; font-weight: bold; }
    </style>
    """
    
    template = css + """
    <div class="ticker">{{ DATA[g.lang]['market'] }}: {{ ticker }}</div>
    <nav><a href="/lang/ar">AR</a> | <a href="/lang/en">EN</a></nav>
    <div class="box">
        <h1>{{ DATA[g.lang]['title'] }}</h1>
        <h2>{{ DATA[g.lang]['vault'] }} ${{ "%.2f"|format(session.get('vault', 0)) }}</h2>
        <form method="post">
            <input name="amount" type="number" placeholder="Enter Amount">
            <br><button type="submit">{{ DATA[g.lang]['invest'] }}</button>
        </form>
    </div>
    """
    return render_template_string(template, DATA=DATA, ticker=ticker)

@app.route("/lang/<l>")
def set_lang(l): session['lang'] = l; return redirect(url_for('/'))

if __name__ == "__main__": app.run()
