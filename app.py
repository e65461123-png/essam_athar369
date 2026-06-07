from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from blueprints.routes import main_bp

app = Flask(__name__)
app.secret_key = 'aether369_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aether369.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

class Wallet(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    balance_usd = db.Column(db.Float, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
