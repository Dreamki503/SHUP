from flask import Blueprint

client_bp = Blueprint('client_bp', __name__, template_folder='templates')

from . import routes
from . import models