from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' 

# Blueprint imports
from RustPlusWeb import RustPlus
from User import User
app.register_blueprint(RustPlus, url_prefix="/rustplus")
app.register_blueprint(User, url_prefix="/user")

@app.route("/")
def index():
    return render_template("index.html")
