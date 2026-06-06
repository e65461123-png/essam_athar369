from flask import Flask
import os
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    # سحب الرابط اللي إنت حطيته في الـ Environment
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    try:
        # محاولة الاتصال
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return "<h1>تهانينا يا وحش! الاتصال بقاعدة البيانات شغال 100%.</h1>"
    except Exception as e:
        return f"<h1>مشكلة في الاتصال: {str(e)}</h1>"

if __name__ == '__main__':
    app.run()
