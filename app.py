from flask import Flask, render_template_string, request, session, redirect, url_for, g

app = Flask(__name__)
app.secret_key = "ATHEER_369_STABLE_CORE"

CONTENT = {
    'ar': {'title': 'منصة ATHEER 369 المالية', 'vault': 'رصيد الخزنة:', 'invest': 'تفعيل التدفق', 'amount': 'أدخل المبلغ', 'lang_label': 'اللغة'},
    'en': {'title': 'ATHEER 369 Financial Portal', 'vault': 'Vault Balance:', 'invest': 'Activate Flow', 'amount': 'Enter Amount', 'lang_label': 'Language'},
    'fr': {'title': 'Portail Financier ATHEER 369', 'vault': 'Solde du coffre:', 'invest': 'Activer le flux', 'amount': 'Montant', 'lang_label': 'Langue'}
}

@app.before_request
def setup_lang(): g.lang = session.get('lang', 'ar')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form.get("amount", 0))
        session['vault'] = session.get('vault', 0) + (amount * 0.10)
    
    # التعديل هنا: استخدام دالة format لضمان عدم حدوث تعارض في الأقواس
    template = """
    <body style="background:#000; color:#0f0; font-family:sans-serif; text-align:center;">
        <nav><a href="/set/ar">AR</a> | <a href="/set/en">EN</a> | <a href="/set/fr">FR</a></nav>
        <h1>%s</h1>
        <div style="border:2px solid #0f0; width:350px; margin:20px auto; padding:20px;">
            <h3>%s $%s</h3>
            <form method="post">
                <input name="amount" placeholder="%s" style="background:#000; color:#fff; border:1px solid #0f0;">
                <button type="submit" style="background:#0f0; border:none; padding:5px 15px;">%s</button>
            </form>
        </div>
    </body>
    """ % (CONTENT[g.lang]['title'], CONTENT[g.lang]['vault'], "{:.2f}".format(session.get('vault', 0)), CONTENT[g.lang]['amount'], CONTENT[g.lang]['invest'])
    
    return render_template_string(template)

@app.route("/set/<lang>")
def set_lang(lang): session['lang'] = lang; return redirect(url_for('index'))

if __name__ == "__main__": app.run()
