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
import website.DAO.productDAO as productDAO
from website.Database import Database



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
"""

@app.route('/api/account', methods=['POST'])
def create_account():
    accountDAO.Create(request.get_json())
    return "success", 400