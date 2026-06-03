from flask import Flask, render_template_string, request, redirect, session, url_for, g

app = Flask(__name__)
app.secret_key = "ATHEER_369_NUCLEAR_CORE"

# نظام اللغات الشامل
LANGUAGES = {
    'ar': {'title': 'ATHEER 369 - منصة الوساطة المالية', 'invest': 'تفعيل التدفق المالي', 'vault': 'الخزنة الخاصة', 'logout': 'تسجيل خروج', 'amount': 'قيمة الاستثمار'},
    'en': {'title': 'ATHEER 369 - Financial Brokerage', 'invest': 'Activate Cash Flow', 'vault': 'Private Vault', 'logout': 'Logout', 'amount': 'Investment Amount'},
    'fr': {'title': 'ATHEER 369 - Courtage Financier', 'invest': 'Activer le flux', 'vault': 'Coffre-fort', 'logout': 'Déconnexion', 'amount': 'Montant'}
}

@app.before_request
def load_lang(): g.lang = session.get('lang', 'ar')

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("username") == "Essam369" and request.form.get("password") == "369369":
            session["logged_in"] = True
            return redirect(url_for('dashboard'))
    return render_template_string("<body style='background:#000; color:#0f0; text-align:center; padding-top:100px;'><h1>LOGIN</h1><form method='post'><input name='username' placeholder='USER'><br><input name='password' type='password' placeholder='PASS'><br><button>ENTER</button></form></body>")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"): return redirect(url_for('home'))
    # منطق الخزنة
    if request.method == "POST":
        amount = float(request.form.get("amount", 0))
        session['vault'] = session.get('vault', 0) + (amount * 0.10)
        return redirect(url_for('dashboard'))
    
    return render_template_string(f"""
    <body style='background:#000; color:#0f0; font-family:monospace; text-align:center;'>
        <nav><a href='/lang/ar'>AR</a> | <a href='/lang/en'>EN</a> | <a href='/lang/fr'>FR</a></nav>
        <h1>{{{{LANGUAGES[g.lang]['title']}}}}</h1>
        <div style='border:1px solid #0f0; width:300px; margin:auto; padding:20px;'>
            <p>{{{{LANGUAGES[g.lang]['vault']}}}}: ${session.get('vault', 0):.2f}</p>
            <form method='post'><input name='amount' placeholder='{{{{LANGUAGES[g.lang]['amount']}}}}'><br>
            <button>{{{{LANGUAGES[g.lang]['invest']}}}}</button></form>
        </div>
        <br><a href='/logout' style='color:red;'>{{{{LANGUAGES[g.lang]['logout']}}}}</a>
    </body>
    """, LANGUAGES=LANGUAGES)

@app.route("/lang/<l>")
def set_lang(l): session['lang'] = l; return redirect(url_for('dashboard'))

@app.route("/logout")
def logout(): session.clear(); return redirect(url_for('home'))

if __name__ == "__main__": app.run()
