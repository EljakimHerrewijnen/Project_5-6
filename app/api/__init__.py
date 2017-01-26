from flask import Blueprint

api = Blueprint('api', __name__, template_folder="templates")

import app.api.endpoints
import app.api.admin