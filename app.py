import os
from flask import Flask, render_template

# نحدد المسار ليبحث داخل المجلد الفرعي essam_athar369 ثم مجلد templates
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'essam_athar369', 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'AETHER_369_SECRET_KEY'

@app.route('/')
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
