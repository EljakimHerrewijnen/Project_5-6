import json
from flask import request, Response, session
from flask_cors import CORS, cross_origin
from app.api import api
from app.api.DAO import *
from app.api.auth import secure


@api.route("/products/<id>")
def product(id):
    product = Models.Product.find(id)
    return Response(product.ToJson(), mimetype='application/json')


@api.route("/products")
def products():
    json_result = json.dumps(productDAO.FindAll(), sort_keys=True, indent=4)
    return Response(json_result, mimetype="application/json")


@api.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return "logged out", 200


@api.route('/user/account', methods=['POST'])
def create_account():
    result = accountDAO.Create(request.get_json())
    if type(result) == sqlite3.Error:
        return "Could not create address", 400
    return "success", 200


@api.route('/user/account', methods=['GET'])
@secure()
def get_account(account):
    json_result = json.dumps(account)
    return Response(json_result, mimetype="application/json")


@api.route('/user/account', methods=['PUT'])
@secure()
def update_account(account):
    post_data = request.get_json()
    post_data['username'] = account['username']
    result = accountDAO.Update(post_data)
    return "Success", 200


@api.route('/login', methods=['POST'])
def login_account():
    post_data = request.get_json()
    username = post_data['username']
    password = post_data['password']
    account = accountDAO.Find(username)
    if password != account['password']:
        return "Invalid password", 403
    session['username'] = username
    return "Success", 200

    
@api.route('/user/address', methods=['POST'])
@secure()
def add_address(account):
    post_data = request.get_json()
    postal_code = post_data["postal_code"]
    house_number = post_data["house_number"]
    address = addressDAO.Find(postal_code, house_number)

    # address does not exist: create address
    if not address:
        addressDAO.Create(post_data)
    result = user_addressDAO.Create(postal_code, house_number, account['username'])
    return "success", 200


@api.route('/user/address', methods=['GET'])
@secure()
def get_address(account):
    result = addressDAO.FindByUser(account.username)
    return Response(json.dumps(result), 200, mimetype='application/json', )


@api.route('/user/address', methods=['DELETE'])
@secure()
def delete_address(account):
    post_data = request.get_json()
    postal_code = post_data["postal_code"]
    house_number = post_data["house_number"]
    result = user_addressDAO.Delete(postal_code, house_number, account['username'])
    return "Success!", 200


@api.route('/user/favorites', methods=['POST'])
@secure()
def add_favorite(account):
    post_data = request.get_json()
    product_id = post_data["product_id"]
    product = productDAO.Find(product_id)
    if not product:
        return "Product does not exist", 404
    result = favoritesDAO.Create(account['username'], product_id)
    return "Success!", 200


@api.route('/user/favorites', methods=['GET'])
@secure()
def get_favorite(account):
    print(account['favorites'])
    return Response(json.dumps(account['favorites']), 200, mimetype='application/json', )
        

@api.route('/user/favorites', methods=['DELETE'])
@secure()
def delete_favorite(account):
    product_id = request.get_json()
    product_id = product_id["product_id"]
    result = favoritesDAO.Delete(account['username'], product_id)
    return "Success", 200
    

@api.route('/user/wishlist', methods=['POST'])
@secure()
def add_wishlist(account):
    postData = request.get_json()
    product_id = postData["product_id"]
    product = productDAO.Find(product_id)
    if (not product):
        return "Product does not exist", 404
    result = wishDAO.Create(account['username'], product_id)
    return "Success!", 200


@api.route('/user/wishlist', methods=['GET'])
@secure()
def get_wishlist(account):
    result = wishDAO.FindByUser(account['username'])
    return Response(json.dumps(result), 200, mimetype='application/json')


@api.route('/user/wishlist', methods=['DELETE'])
@secure()
def delete_wishlist(account):
    product_id = request.get_json()
    product_id = product_id["product_id"]
    result = wishDAO.Delete(account['username'], product_id)
    return "Success", 200
    

@api.route('/user/orders', methods=['POST'])
@secure()
def add_order(account):
    print(request)
    postData = request.get_json()
    result = orderDAO.Create(account['username'], postData)
    return Response(json.dumps(result), 200, mimetype='application/json')


@api.route('/user/orders', methods=['GET'])
@secure()
def get_orders(account):
    orders = orderDAO.FindByUser(account['username'])
    return Response(json.dumps(result), 200, mimetype='application/json', )


@api.route('/user/orders/<order_id>')
@secure()
def get_order(account, order_id):
    print(order_id)
    order = orderDAO.Find(order_id)
    if (order['username'] == account['username']):
        return Response(json.dumps(order), 200, mimetype='application/json', )
    return "Unauthorized", 401