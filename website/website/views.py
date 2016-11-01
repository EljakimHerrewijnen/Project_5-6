from flask import render_template
from website import app

@app.route('/')
def index():
    return render_template('BaseContainer.html')

@app.route('/products/<id>')
def products(id):
    print(id)
    return render_template('ProductDetailsViewContainer.html', id=id)

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/account/register')
def register():
    return render_template('register.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')