from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "ATHEER 369 Platform is Online"

if __name__ == '__main__':
    app.run()
