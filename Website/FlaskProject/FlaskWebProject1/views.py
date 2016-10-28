from flask import render_template
from FlaskWebProject1 import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/contact')
def contact():
    print('Rendering Contacts')
    return render_template('contact.html')

@app.route('/deals')
def deals():
    print("Generating deals")
    return render_template('deals.html')

@app.route('/account')
def account():
    return render_template('account.html')
