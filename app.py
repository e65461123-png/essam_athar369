from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    user = request.form.get('username')
    pw = request.form.get('password')
    new_user = User(username=user, password=pw)
    db.session.add(new_user)
    db.session.commit()
    return "تم التسجيل بنجاح!"

if __name__ == '__main__':
    app.run()
