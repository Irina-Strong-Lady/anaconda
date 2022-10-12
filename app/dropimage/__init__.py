from flask import Blueprint

dropimage = Blueprint('dropimage', __name__, static_folder='static', static_url_path='/static')

from . import views, errors, validate