from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "messages.json"

# --- تحميل وحفظ الرسائل ---
def load_msgs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_msgs(msgs):
    with open(DATA_FILE, 'w') as f:
        json.dump(msgs, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    msgs = load_msgs()
    if request.method == 'POST':
        user = escape(request.form.get('user', '').strip())
        content = escape(request.form.get('content', '').strip())
        if user and content:
            msgs.append({
                "user": user,
                "content": content,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_msgs(msgs)
        return redirect(url_for('home'))
    return render_template('index.html', msgs=msgs)

@app.route('/clear')
def clear():
    save_msgs([])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
