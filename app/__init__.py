from flask import Flask
import os

def create_app():
    # نحدد المسار بدقة بناءً على وجود المجلدات داخل app
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')

    app = Flask(__name__, 
                template_folder=template_dir, 
                static_folder=static_dir)

    return app
