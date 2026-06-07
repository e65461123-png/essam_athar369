from flask import Flask
from blueprints.routes import main_bp  # استيراد الـ Blueprint

app = Flask(__name__)

# تسجيل الـ Blueprint
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
