from flask import Blueprint

api = Blueprint('api', __name__)

import app.api.endpoints
import app.api.admin