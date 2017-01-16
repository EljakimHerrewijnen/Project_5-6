from flask import Blueprint

website = Blueprint('website', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

import app.website.views