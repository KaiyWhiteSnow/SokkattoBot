from flask import Flask, render_template
from .web.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
