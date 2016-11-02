from flask import request
from flask import Response
from flask import session
from website import Models
from website import app
from flask_cors import CORS, cross_origin
import json

app.secret_key = "Kz9bEtc3spQ2bQdA8VxyMqDh76AeAvYK15Qfe2sBwXF5rTvKkXwq"

@app.route("/API/Products/<id>")
def ProductRouteHandler(id):
    product = Models.Product.find(id)
    return Response(product.ToJson(), mimetype='application/json')

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


@app.route("/API/account/<id>")
def accountRouteHandler(id):
    db = Database.Database()
    db.where("username", id)
    result = db.get_all("account")

    db.where("username", id)
    result[0]["Orders"] = db.get_all("orders")

    db.where("username", id)
    db.join("product p", "f.product_id = p.product_id")
    result[0]["favorits"] = db.get_all("favorites f", "p.product_id, p.name")

    db.where('postal_code', result[0]['postal_code'])
    db.where('house_number', result[0]['house_number'])
    result[0]["address"] = db.get_all("address")

    db.where("username", id)
    db.join("product p", "w.product_id = p.product_id")
    result[0]["Wishlist"] = db.get_all("wishes w", "p.product_id, p.name")

    return Response(db.to_jsonarray(result), mimetype='application/json')

>>>>>>> origin/account_retrieval
