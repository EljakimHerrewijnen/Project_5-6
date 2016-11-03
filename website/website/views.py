from flask import render_template
from website import app

@app.route('/')
def index():
    return render_template('BaseContainer.html')

@app.route('/products/<id>')
def products(id):
    print(id)
    return render_template('ProductDetailsViewContainer.html', id=id)

@app.route('/login')
def login():
    return render_template("BaseContainerLogin.html");