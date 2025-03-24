from flask import Blueprint
from flask_login import current_user

admin_bp = Blueprint('admin_bp', __name__,url_prefix="/admin", template_folder='templates', static_folder='static')

from . import routes