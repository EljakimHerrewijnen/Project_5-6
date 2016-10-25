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
    aromas = request.args.get("Aromas").split(" ")

    products = Models.Product.get_all()
    if (name):
        products = filter(lambda product: product.has_name(Name), products)

    if (minPrice and maxPrice):
        products = filter(lambda product: product.has_price(minPrice, maxPrice), products)

    if (aromas):
        products = filter(lambda product: product.has_aromas(aromas, False), products)

    if (origin):
        products = filter(lambda product: product.has_origin(origin), products)

    return "<pre>" + Models.Product.ArrayToJson(products)

if __name__ == "__main__":
    app.run()