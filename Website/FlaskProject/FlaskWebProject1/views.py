from flask import render_template
from FlaskWebProject1 import app

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products/<id>')
def products(id):
    return render_template('products.html', id=id)