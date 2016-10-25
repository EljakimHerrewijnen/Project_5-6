from flask import render_template
from FlaskWebProject1 import app

@app.route('/brands/<name>')
def brands(name):
    return render_template('brands.html', name=name)


