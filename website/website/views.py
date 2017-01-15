from flask import render_template
from website import app

@app.route('/')
def index():
    return render_template('BaseContainer.html')

@app.route('/products/<id>')
def products(product_id):
    print(id)
    return render_template('ProductDetailsViewContainer.html', id=product_id)

@app.route('/login')
def login():
    return render_template("BaseContainerLogin.html");

@app.route('/cart')
def cart():
    return render_template("BaseContainerCart.html");

@app.route('/account')
def user_page():
    return render_template("BaseContainerAccount.html")

@app.route('/order/<id>')
def order_page(id):
    return render_template("BaseContainerOrderDetail.html", id=id)

@app.route('/orderview')
def OrderView():
    return render_template("BaseContainerOrder.html")

@app.route('/test', defaults={'path': ''})
@app.route('/test/', defaults={'path': ''})
@app.route('/test/<path:path>')
def test(path):
    return render_template("test.html")