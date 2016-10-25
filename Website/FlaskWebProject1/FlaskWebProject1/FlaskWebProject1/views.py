from flask import render_template
from FlaskWebProject1 import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/brands/<name>/<des>')
def brands(name, des):
    return render_template('brands.html', name=name, des=des)

@app.route('/admin')
def admin():
    return render_template('admin.html')

