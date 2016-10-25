from flask import Flask
from flask import request
import Models
import json

app = Flask("webshop")  

@app.route("/API/Products")
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

if __name__ == "__main__":
    app.run()