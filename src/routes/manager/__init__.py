from flask import Blueprint

# Register the "manager" blueprint
manager = Blueprint("manager", __name__, url_prefix='/manager')

from . import routes  # Import routes to register them with the blueprint
