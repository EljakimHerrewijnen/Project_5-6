from flask import request
from FlaskWebProject1 import Models
from FlaskWebProject1 import app
from flask_cors import CORS, cross_origin
import json

@app.route("/API/Products")
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def ProductsRouteHandler():
    name = request.args.get("Name")
    minPrice = request.args.get("Min")
    maxPrice = request.args.get("Max")
    origin = request.args.get("Origin")
    aromas = request.args.get("Aromas")
    description = request.args.get("Description")

    products = Models.Product.get_all()
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
        products = filter(lambda product: product.has_aromas(aromas.split(" "), False), products)

    if (origin):
        products = filter(lambda product: product.has_origin(origin), products)

    if (description):
        products = filter(lambda product: product.description_contains(description), products)

    return "<pre>" + Models.Product.ArrayToJson(products)