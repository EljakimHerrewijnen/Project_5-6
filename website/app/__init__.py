from flask import Flask, render_template
from flask_cors import CORS, cross_origin

from app.website.views import test
from app.docs import docs
from app.api import api

app = Flask(__name__)
cors = CORS(app)
app.debug = True

app.register_blueprint(docs, url_prefix='/docs')
app.register_blueprint(api, url_prefix='/api')
app.secret_key = "secret test key"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def dix(path):
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)