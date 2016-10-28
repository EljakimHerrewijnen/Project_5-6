from flask import render_template
from FlaskWebProject1 import app
from Database import get_coffee_by_id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/brands/<name>/<des>')
def brands(name, des):
    return render_template('brands.html', name=name, des=des)

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

@app.route('/API/USER/<id>')
def Coffee_By_ID(id):
    res = Database.get_coffee_by_id(id)
    return jsonify(json_list = res.all())
    print(res)