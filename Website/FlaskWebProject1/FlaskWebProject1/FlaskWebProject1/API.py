from flask import request
from flask import Response
from FlaskWebProject1 import Models
from FlaskWebProject1 import app
from flask_cors import CORS, cross_origin
import json

@app.route("/API/Products")
def ProductsRouteHandler():
    id = request.args.get("id")
    name = request.args.get("name")
    minPrice = request.args.get("min")
    maxPrice = request.args.get("max")
    origin = request.args.get("origin")
    aromas = request.args.get("aromas")
    description = request.args.get("description")
    amount = request.args.get("size")
    offset = request.args.get("offset")

    products = Models.Product.find(id)

    if (name):
        products = filter(lambda product: product.has_name(name), products)

    if (minPrice or maxPrice):
        if (minPrice and maxPrice):
            products = filter(lambda product: product.has_price(float(minPrice), float(maxPrice)), products)
        elif (minPrice):
            products = filter(lambda product: product.has_price(float(minPrice)), products)
        else:
            products = filter(lambda product: product.has_price(0, float(maxPrice)), products)
        
    if (aromas):
        products = filter(lambda product: product.has_aromas(aromas.split(" "), True), products)

    if (origin):
        products = filter(lambda product: product.has_origin(origin), products)

    if (description):
        products = filter(lambda product: product.description_contains(description), products)

    if (amount):
        if (offset):
            offset = int(offset)
            products = products[offset : offset + int(amount)]
        else:
            products = products[0:int(amount)]
    
    return Response(Models.Product.ArrayToJson(products), mimetype='application/json')