from flask import request
from flask import Response
from flask import session
from app.api import api
from flask_cors import CORS, cross_origin
import json
from app.api.DAO import accountDAO
from app.api.DAO import addressDAO
from app.api.DAO import favoritesDAO
from app.api.DAO import productDAO
from app.api.DAO import user_addressDAO
from app.api.DAO import wishDAO
from app.api.DAO import orderDAO

from app.api.database import Database
import sqlite3

@api.route("/products/<id>")
def ProductRouteHandler(id):
    product = Models.Product.find(id)
    return Response(product.ToJson(), mimetype='application/json')


@api.route("/products")
def Products():
    jsonResult = json.dumps(productDAO.FindAll(), sort_keys=True, indent=4)
    return Response(jsonResult, mimetype="application/json")


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
def getAccount():
    sessionUsername = GetCurrentUsername()
    if not sessionUsername:
        return "Unauthorized", 401

    completeAccount = accountDAO.Find(sessionUsername)
    jsonResult = json.dumps(completeAccount)
    return Response(jsonResult, mimetype="application/json")

@api.route('/user/account', methods=['PUT'])
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

@api.route('/login', methods=['POST'])
def loginAccount():
    postData = request.get_json()
    username = postData['username']
    password = postData['password']

    account = accountDAO.Find(username)
    if not account:
        return "Invalid Username", 400

    if not password == account['password']:
        return "Invalid password", 400

    session['username'] = username
    return "Success", 200

# Get addresses of a user
@api.route('/user/address', methods=['POST'])
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
@api.route('/user/address', methods=['GET'])
def get_address():
    username = GetCurrentUsername()
    if (not username):
        return "Unauthorized", 401

    result = addressDAO.FindByUser(username)
    if type(result) == sqlite3.Error:
        return "Could not find addresses", 400

    return Response(json.dumps(result), 200, mimetype='application/json', )

# Delete address of a user
@api.route('/user/address', methods=["DELETE"])
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

@api.route('/user/favorites', methods=['POST'])
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


@api.route('/user/favorites', methods=['GET'])
def get_favorite():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401

    result = favoritesDAO.FindByUser(username)
    if type(result) == sqlite3.Error:
        return "Database error, could not find favorites", 400
    return Response(json.dumps(result), 200, mimetype='application/json', )
        

@api.route('/user/favorites', methods=['DELETE'])
def delete_favorite():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401
    product_id = request.get_json()
    product_id = product_id["product_id"]
    result = favoritesDAO.Delete(username, product_id)
    return "Success", 200
    

@api.route('/user/wishlist', methods=['POST'])
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


@api.route('/user/wishlist', methods=['GET'])
def get_wishlist():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401

    result = wishDAO.FindByUser(username)
    if type(result) == sqlite3.Error:
        return "Database error, could not find wishes", 400
    return Response(json.dumps(result), 200, mimetype='application/json', )


@api.route('/user/wishlist', methods=['DELETE'])
def delete_wishlist():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401
    product_id = request.get_json()
    product_id = product_id["product_id"]
    result = wishDAO.Delete(username, product_id)
    return "Success", 200
    

@api.route('/user/orders', methods=['POST'])
def add_order():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401
    postData = request.get_json()
    result = orderDAO.Create(username, postData)
    if type(result) == sqlite3.Error:
        return "Database error, could not create order", 400
    return "Success!", 200


@api.route('/user/orders', methods=['GET'])
def get_orders():
    username = GetCurrentUsername()
    if not username:
        return "Unauthorized", 401
    orders = orderDAO.FindByUser(username)
    if type(orders) == sqlite3.Error:
            return "Database error, could not find orders", 400
    return Response(json.dumps(result), 200, mimetype='application/json', )


@api.route('/user/orders/<order_id>')
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
