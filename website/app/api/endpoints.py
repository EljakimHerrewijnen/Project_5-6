import json
from flask import request, Response, session
from flask_cors import CORS, cross_origin
from app.api import api
from app.api.DAO import *
from app.api.auth import secure
from app.api.database import Database


"""
PRODUCTS
"""

@api.route("/products")
def products():
    json_result = json.dumps(productDAO.FindAll(), sort_keys=True, indent=4)
    return Response(json_result, mimetype="application/json")

@api.route("/products/<id>")
def product(id):
    product = productDAO.Find(id)
    product = json.dumps(product, sort_keys=True, indent=4)
    return Response(product, mimetype='application/json')

"""
AUTHENTICATION
"""

@api.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return "logged out", 200

@api.route('/login', methods=['POST'])
def login_account():
    post_data = request.get_json()
    print(post_data)
    username = post_data['username']
    password = post_data['password']
    account = accountDAO.Find(username)
    if password != account['password']:
        return "Invalid password", 403
    session['username'] = username
    return "Success", 200

"""
ACCOUNT
"""

@api.route('/account', methods=['POST'])
def create_account():
    result = accountDAO.Create(request.get_json())
    return "success", 200

@api.route('/account', methods=['GET'])
@secure()
def get_account(account):
    account['wishlist'] = wishDAO.FindByUser(account['username'])
    account['favorites'] = favoritesDAO.FindByUser(account['username'])
    account['orders'] = orderDAO.FindByUser(account['username'])
    account['addresses'] = addressDAO.FindByUser(account['username'])
    json_result = json.dumps(account)
    return Response(json_result, mimetype="application/json")

@api.route('/account', methods=['PUT'])
@secure()
def update_account(account):
    post_data = request.get_json()
    post_data['username'] = account['username']
    result = accountDAO.Update(post_data)
    return "Success", 200

@api.route('/account/address', methods=['POST'])
@secure()
def add_address(account):
    post_data = request.get_json()
    postal_code = post_data["postalCode"]
    house_number = post_data["houseNumber"]
    address = addressDAO.Find(postal_code, house_number)

    # address does not exist: create address
    if not address:
        addressDAO.Create(post_data)
    result = user_addressDAO.Create(postal_code, house_number, account['username'])
    return "success", 200

@api.route('/account/address', methods=['GET'])
@secure()
def get_address(account):
    result = addressDAO.FindByUser(account['username'])
    return Response(json.dumps(result), 200, mimetype='application/json', )

@api.route('/account/address', methods=['DELETE'])
@secure()
def delete_address(account):
    post_data = request.get_json()
    postal_code = post_data["postalCode"]
    house_number = post_data["houseNumber"]
    result = user_addressDAO.Delete(postal_code, house_number, account['username'])
    return "Success!", 200

@api.route('/account/favorites', methods=['POST'])
@secure()
def add_favorite(account):
    post_data = request.get_json()
    productId = post_data["id"]
    product = productDAO.Find(productId)
    if not product:
        return "Product does not exist", 404
    result = favoritesDAO.Create(account['username'], productId)
    return "Success!", 200

@api.route('/account/favorites', methods=['GET'])
@secure()
def get_favorite(account):
    result = favoritesDAO.FindByUser(account['username'])
    return Response(json.dumps(result), 200, mimetype='application/json')

@api.route('/account/favorites', methods=['DELETE'])
@secure()
def delete_favorite(account):
    productId = request.get_json()
    productId = productId["id"]
    result = favoritesDAO.Delete(account['username'], productId)
    return "Success", 200

@api.route('/account/wishlist', methods=['POST'])
@secure()
def add_wishlist(account):
    postData = request.get_json()
    productId = postData["id"]
    product = productDAO.Find(productId)
    if (not product):
        return "Product does not exist", 404
    result = wishDAO.Create(account['username'], productId)
    return "Success!", 200

@api.route('/account/wishlist', methods=['GET'])
@secure()
def get_wishlist(account):
    result = wishDAO.FindByUser(account['username'])
    return Response(json.dumps(result), 200, mimetype='application/json')

@api.route('/account/wishlist', methods=['DELETE'])
@secure()
def delete_wishlist(account):
    productId = request.get_json()
    productId = productId["id"]
    result = wishDAO.Delete(account['username'], productId)
    return "Success", 200

@api.route('/account/order', methods=['POST'])
@secure()
def add_order(account):
    postData = request.get_json()
    print(postData)
    result = orderDAO.Create(account['username'], postData)
    return Response(json.dumps(result), 200, mimetype='application/json')

@api.route('/account/order', methods=['GET'])
@secure()
def get_orders(account):
    orders = orderDAO.FindByUser(account['username'])
    return Response(json.dumps(orders), 200, mimetype='application/json')

@api.route('/account/order/<order_id>')
@secure()
def get_order(account, order_id):
    print(order_id)
    order = orderDAO.Find(order_id)
    if (order['username'] == account['username']):
        return Response(json.dumps(order), 200, mimetype='application/json', )
    return "Unauthorized", 401

"""
PUBLIC WISH LISTS
"""

@api.route('/wishlist')
def get_public_wishlists():
    db = Database()
    db.where("wishlist_public", 1)
    accounts = db.getAll("account", select = "username, name")
    json_result = json.dumps(accounts, sort_keys=True, indent=4)
    return Response(json_result, mimetype="application/json")

@api.route('/wishlist/<username>')
def get_public_wishlist(username):
    db = Database()
    account = accountDAO.Find(username)
    print(account)
    if account['wishlistPublic']:
        response = {
            "wishlist" : wishDAO.FindByUser(username),
            "name" : account["name"],
            "surname" : account['surname']
        }
        json_result = json.dumps(response, sort_keys=True, indent=4)
        return Response(json_result, mimetype='application/json')
    else:
        return "Unauthorized", 401