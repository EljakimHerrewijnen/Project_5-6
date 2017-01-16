from flask import Blueprint, render_template

docs = Blueprint('docs', __name__, template_folder='templates', static_folder='static')

@docs.route('/api')
def api():
    return render_template('index.html')