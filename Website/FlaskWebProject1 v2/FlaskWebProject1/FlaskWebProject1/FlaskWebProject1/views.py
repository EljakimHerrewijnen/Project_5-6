from flask import render_template
from FlaskWebProject1 import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product/<id>')
def product(id):
    return render_template('product.html', id=id)

@app.route('/admin')
def admin():
    return render_template('admin.html')

