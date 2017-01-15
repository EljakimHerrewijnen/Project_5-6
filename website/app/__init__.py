from flask import Flask
from flask_cors import CORS, cross_origin

from app.website import website
from app.docs import docs
from app.api import api

app = Flask(__name__, static_folder='')
cors = CORS(app)
app.debug = True

app.register_blueprint(website, url_prefix='/')
app.register_blueprint(docs, url_prefix='/docs')
app.register_blueprint(api, url_prefix='/api')
app.secret_key = "secret test key"

if __name__ == "__main__":
    app.run(debug=True)