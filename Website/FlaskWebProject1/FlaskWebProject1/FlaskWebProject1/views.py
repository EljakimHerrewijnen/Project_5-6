from flask import render_template
from FlaskWebProject1 import app
from Database import get_coffee_by_id
from flask import request

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

@app.route('/API/user')
def Coffee_By_ID(id):
    print(request)
    id = request.args.get('id')
    aroma = request.args.get('aroma')
    coffee_name = request.args.get('name')
    description = request.args.get('description')
    price = request.args.get('price')
    roast = request.args.get('roast')
    origin = request.args.get('origin')
    picture = request.args.get('picture')
    coffee_id = request.args.get('coffee_id')
    aroma_id = request.args.get('aroma_id')

    if(request = request['GETALL']):
        res = Database.get_all()
        #return jsonify(res)
    if (request = request['id']):
        res = Database.get_coffee_by_id(id)
        print(res)
        #return jsonify(json_list = res.all()) 
    elif(request = request['aroma']):
        Database.where('name', aroma)
        res = Database.get_all('aroma')
    elif(request = request['coffee_name']):
        Database.Where('name', coffee_name)
        res = Database.get_all('coffee')
    elif(request = request['description']):
        Database.where('description', description)
        res = Database.get_all('coffee')
    elif(request = request['price']):
        Database.where('price', price)
        res = Database.get_all('coffee')
    elif(request = request['roast']):
        Database.where('roast', roast)
        res = Database.get_all('coffee')
    elif(request = request['origin']):
        Database.where('origin', origin)
        res = Database.get_all('coffee')
    elif(request = request['picture']):
        Database.where('picture', picture)
        res = Database.get_all('coffee')
    elif(request = request['coffee_id']):
        Database.where('coffee_id', coffee_id)
        res = Database.get_all('coffee')
    elif(request = request['aroma_id']):
        Database.where('aroma_id', aroma_id)
        res = Database.get_all('aroma')


