from flask import Flask, render_template
from .web.auth import auth
from .web.manager import manager
from .config import logger_config
import logging

# Configure loggers - This must run before SQLAlchemy is initialized
logger_config.configure_logger(
    [
        "Sokkatto.manager",
        "Sokkatto.factory",
        "Sokkatto.login",
        "Sokkatto",
        "Sokkatto.database",
        "sqlalchemy"
    ]
)

logger: logging.Logger = logging.getLogger("Sokkatto")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TheApplePie' 

app.register_blueprint(auth)
app.register_blueprint(manager)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
