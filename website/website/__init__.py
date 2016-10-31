"""
The flask application package.
"""
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

import website.views
import website.API
import website.authentication