from flask import request
from flask import Response
from flask import session
from website import Models
from website.models.account import Account
from website.models.account import Address
from website import app
from flask_cors import CORS, cross_origin
import json
import website.DAO.accountDAO as accountDAO
import website.DAO.addressDAO as addressDAO
import website.DAO.favoritesDAO as favoritesDAO
import website.DAO.productDAO as productDAO
import website.DAO.user_addressDAO as user_addressDAO
import website.DAO.wishDAO as wishDAO
import website.DAO.orderDAO as orderDAO


from website.Database import Database
import sqlite3



app.secret_key = "Kz9bEtc3spQ2bQdA8VxyMqDh76AeAvYK15Qfe2sBwXF5rTvKkXwq"

@app.route("/API/Products/<id>")
def ProductRouteHandler(id):
    product = Models.Product.find(id)
    return Response(product.ToJson(), mimetype='application/json')


@app.route("/API/Products")
def Products():
    jsonResult = json.dumps(productDAO.FindAll(), sort_keys=True, indent=4)
    return Response(jsonResult, mimetype="application/json")
    

"""

@app.route("/API/Products")
def ProductsRouteHandler():
    name = request.args.get("name")
    minPrice = request.args.get("min")
    maxPrice = request.args.get("max")
    origin = request.args.get("origin")
    aromas = request.args.get("aromas")
    description = request.args.get("description")
    amount = request.args.get("size")
    offset = request.args.get("skip")

    products = Models.Product.get_all()

    if (name):
        products = list(filter(lambda product: product.has_name(name), products))

    if (minPrice or maxPrice):
        if (minPrice and maxPrice):
            products = list(filter(lambda product: product.has_price(float(minPrice), float(maxPrice)), products))
        elif (minPrice):
            products = list(filter(lambda product: product.has_price(float(minPrice)), products))
        else:
            products = list(filter(lambda product: product.has_price(0, float(maxPrice)), products))
        
    if (aromas):
        products = list(filter(lambda product: product.has_aromas(aromas.split(" "), True), products))

    if (origin):
        products = list(filter(lambda product: product.has_origin(origin), products))

    if (description):
        products = list(filter(lambda product: product.description_contains(description), products))

    if (amount):
        if (offset):
            offset = int(offset)
            products = products[offset : offset + int(amount)]
        else:
            products = products[0:int(amount)]
    
    return Response(Models.Product.ArrayToJson(products), mimetype='application/json')

"""
#@app.route("/API/account/<id>")
#def accountRouteHandler(id):
#    db = Database.Database()
#    db.where("username", id)
#    result = db.get_all("account")
#
#    db.where("username", id)
#    result[0]["Orders"] = db.get_all("orders")
#
#    db.where("username", id)
#    db.join("product p", "f.product_id = p.product_id")
#    result[0]["favorits"] = db.get_all("favorites f", "p.product_id, p.name")
#
#    db.where('postal_code', result[0]['postal_code'])
#    db.where('house_number', result[0]['house_number'])
#    result[0]["address"] = db.get_all("address")
#
#    db.where("username", id)
#    db.join("product p", "w.product_id = p.product_id")
#    result[0]["Wishlist"] = db.get_all("wishes w", "p.product_id, p.name")
#
#    return Response(db.to_jsonarray(result), mimetype='application/json')

"""
@app.route('/api/account', methods=['POST'])
def post_account():

    db = Database()
    db.delete("account")
    db.delete("address")

    account = ""
    try:
        account = Account.fromForm(request.form)

    except:
        print(sys.exc_info())
        return "Invalid form data supplied", 400

    # add to D
    # check if address exists, if not create it
    try:
        addressDAO.Create(account.address)
    except:
        print(sys.exc_info())
        return "Could not create address", 400

    try:
        accountDAO.Create(account)
    except:
        print(sys.exc_info())
        return "Could not create user", 400

    print(account.toDict())
    return "Successfully created an account!", 200


@app.route('/api/account', methods=['GET'])
def get_account():
    db = Database()
    account = accountDAO.Find("bart")
    return account.toJson(), 200

#Chiel en Eljakim
@app.route('/api/cart', methods=['GET'])
def get_cart():
    db = Database()
    #Dev 
"""

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return "logged out", 200


@app.route('/api/user/account', methods=['POST'])
def create_account():
    result = accountDAO.Create(request.get_json())
    if type(result) == sqlite3.Error:
        return "Could not create address", 400

    return "success", 200


@app.route('/api/user/account', methods=['GET'])
def getAccount():
    sessionUsername = GetCurrentUsername()
    if not sessionUsername:
        return "Unauthorized", 401

    completeAccount = accountDAO.Find(sessionUsername)
    jsonResult = json.dumps(completeAccount)
    return Response(jsonResult, mimetype="application/json") 


@app.route('/api/user/account', methods=['PUT'])
def updateAccount():
    sessionUsername = GetCurrentUsername()
    if not sessionUsername:
        return "Unauthorized", 401
    postData = request.get_json()
    postData['username'] = sessionUsername
    result = accountDAO.Update(postData)
    if type(result) == sqlite3.Error:
        return "Could not update user information", 400
    return "Success", 200


@app.route('/api/login', methods=['POST'])
def loginAccount():
    postData = request.get_json()
    print(postData)
    username = postData['username']
    password = postData['password']
    
    account = accountDAO.Find(username)
    if not account:
        return "Invalid Username", 400

    if not (password == account['password']):
        return "Invalid password", 400
    
    session['username'] = username
    return "Success", 200

    
# Get addresses of a user
@app.route('/api/user/address', methods=['POST'])
def add_address():
    username = GetCurrentUsername()
    if (not username):
        return "Unauthorized", 401

    postData = request.get_json()
    postal_code = postData["postal_code"]
    house_number = postData["house_number"]

    address = addressDAO.Find(postal_code, house_number)

    # address does not exist: create address
    result = None
    if (not address):
        result = addressDAO.Create(postData)
        address = addressDAO.Find(postal_code, house_number)
        if type(result) == sqlite3.Error:
            return "Could not create address", 400
    
    if type(result) == sqlite3.Error:
        return "Could not get address", 400

    result = user_addressDAO.Create(postal_code, house_number, username)

    if type(result) == sqlite3.Error:
        return "Could not add address to user", 400

    return "success", 200

# Add address to user (and create if not exists)
@app.route('/api/user/address', methods=['GET'])
def get_address():
    username = GetCurrentUsername()
    if (not username):
        return "Unauthorized", 401

    result = addressDAO.FindByUser(username)
    if type(result) == sqlite3.Error:
        return "Could not find addresses", 400

    return Response(json.dumps(result), 200, mimetype='application/json', )

# Delete address of a user
@app.route('/api/user/address', methods=["DELETE"])
def delete_address():
    username = GetCurrentUsername()
    if (not username):
        return "Unauthorized", 401
    postData = request.get_json()
    postal_code = postData["postal_code"]
    house_number = postData["house_number"]
    result = user_addressDAO.Delete(postal_code, house_number, username)
    if type(result) == sqlite3.Error:
        return "Could not delete address", 400

    return "Success!", 200


@app.route('/api/user/favorites', methods=['POST'])
def add_favorite():
    username = GetCurrentUsername()
    if (not username):
        return "Unauthorized", 401
    postData = request.get_json()
    product_id = postData["product_id"]
    product = productDAO.Find(product_id)
    if type(product) == sqlite3.Error:
        return "Database error, could not find product", 400

    if (not product):
        return "Product does not exist", 404

    result = favoritesDAO.Create(username, product_id)
    
    if type(result) == sqlite3.Error:
        return "Could not add product to favorites", 400
    return "Success!", 200


@app.route('/api/user/favorites', methods=['GET'])
def get_favorite():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401

    result = favoritesDAO.FindByUser(username)
    if type(result) == sqlite3.Error:
        return "Database error, could not find favorites", 400
    return Response(json.dumps(result), 200, mimetype='application/json', )
        

@app.route('/api/user/favorites', methods=['DELETE'])
def delete_favorite():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401
    product_id = request.get_json()
    product_id = product_id["product_id"]
    result = favoritesDAO.Delete(username, product_id)
    return "Success", 200
    

@app.route('/api/user/wishlist', methods=['POST'])
def add_wishlist():
    username = GetCurrentUsername()
    if (not username):
        return "Unauthorized", 401
    postData = request.get_json()
    product_id = postData["product_id"]
    product = productDAO.Find(product_id)
    if type(product) == sqlite3.Error:
        return "Database error, could not find product", 400
    if (not product):
        return "Product does not exist", 404

    result = wishDAO.Create(username, product_id)
    
    if type(result) == sqlite3.Error:
        return "Could not add product to wishlist", 400
    return "Success!", 200


@app.route('/api/user/wishlist', methods=['GET'])
def get_wishlist():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401

    result = wishDAO.FindByUser(username)
    if type(result) == sqlite3.Error:
        return "Database error, could not find wishes", 400
    return Response(json.dumps(result), 200, mimetype='application/json', )


@app.route('/api/user/wishlist', methods=['DELETE'])
def delete_wishlist():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401
    product_id = request.get_json()
    product_id = product_id["product_id"]
    result = wishDAO.Delete(username, product_id)
    return "Success", 200
    

@app.route('/api/user/orders', methods=['POST'])
def add_order():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401
    postData = request.get_json()
    result = orderDAO.Create(username, postData)
    if type(result) == sqlite3.Error:
        return "Database error, could not create order", 400
    return "Success!", 200


@app.route('/api/user/orders', methods=['GET'])
def get_orders():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401
    orders = orderDAO.FindByUser(username)
    if type(orders) == sqlite3.Error:
            return "Database error, could not find orders", 400
    return Response(json.dumps(result), 200, mimetype='application/json', )


@app.route('/api/user/orders/<order_id>')
def get_order(order_id):
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401
    order = orderDAO.Find(order_id)
    if type(order) == sqlite3.Error:
        return "Database error, could not find order", 400
    if (order['username'] == username):
        return Response(json.dumps(order), 200, mimetype='application/json', )
    return "Unauthorized", 401


# Attempts to get the current username belonging to the session
def GetCurrentUsername():
    if "username" in session:
        user = accountDAO.Find(session["username"])
        if (user):
            return session["username"]
    return None
