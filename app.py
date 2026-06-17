from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

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

# --- قوالب HTML مدمجة (شكل محترم) ---
HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>🔥 موقع الأبطال</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1e1e2f; color: #fff; text-align: center; padding: 50px; }
        .card { background: #2d2d44; padding: 30px; border-radius: 20px; max-width: 600px; margin: auto; box-shadow: 0 0 30px #7f5af0; }
        input, textarea { width: 90%; padding: 12px; margin: 10px 0; border-radius: 10px; border: none; }
        button { background: #7f5af0; color: #fff; padding: 12px 30px; border: none; border-radius: 30px; font-weight: bold; cursor: pointer; }
        .msg { background: #3a3a55; margin: 10px 0; padding: 15px; border-radius: 15px; text-align: left; }
        a { color: #7f5af0; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 مرحباً يا {{ name }}!</h1>
        <p>ده مش طفولي، ده موقع جاد بالكامل 😎</p>
        <hr>
        <h3>💬 سيب رسالتك:</h3>
        <form method="POST">
            <input type="text" name="user" placeholder="اسمك" required><br>
            <textarea name="content" rows="3" placeholder="اكتب أي حاجة..." required></textarea><br>
            <button type="submit">💥 انشر الرسالة</button>
        </form>
        <hr>
        <h3>📜 رسائل الأبطال:</h3>
        {% if msgs %}
            {% for m in msgs %}
                <div class="msg"><strong>{{ m.user }}</strong>: {{ m.content }}</div>
            {% endfor %}
        {% else %}
            <p>✋ مفيش رسائل لسه، كن أول بطل!</p>
        {% endif %}
        <br><a href="{{ url_for('clear') }}" style="color: #ff6b6b;">🗑️ مسح الكل (لعبة)</a>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    msgs = load_msgs()
    if request.method == 'POST':
        user = request.form.get('user')
        content = request.form.get('content')
        if user and content:
            msgs.append({"user": user, "content": content})
            save_msgs(msgs)
        return redirect(url_for('home'))
    return render_template_string(HOME_PAGE, msgs=msgs, name="يا وحش")

@app.route('/clear')
def clear():
    save_msgs([])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
