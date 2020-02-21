#!../venv/bin/python3
from flask import Flask

app = Flask(__name__)

from app import routes

#@app.route('/')
#def index():
#    return "Hello World!"
#
#if __name__ == '__main__':
#    app.run(debug=True)