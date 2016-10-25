"""
The flask application package.
"""
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/API": {"origins": "*"}})

import FlaskWebProject1.views
import FlaskWebProject1.API