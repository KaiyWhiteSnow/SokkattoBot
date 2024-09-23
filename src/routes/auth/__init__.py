from flask import Blueprint

# Register the "auth" blueprint
auth = Blueprint("authorization", __name__, url_prefix='/authorization')

from . import routes  # Import routes to register them with the blueprint
