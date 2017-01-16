from flask import render_template
from app.website import website

@website.route('/404')
def notFound():
    return "404!"

@website.route('/', defaults={'path': ''})
@website.route('/<path:path>')
def test(path):
    return render_template("base.html")