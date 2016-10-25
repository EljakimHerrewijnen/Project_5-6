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
    products = Models.Product.get_all()
    if (name):
        products = Models.Product.get_by_name(name, products)

    if (minPrice and maxPrice):
        products = Models.Product.get_by_price(float(minPrice), float(maxPrice), products)

    return "<pre>" + Models.Product.ArrayToJson(products)

if __name__ == "__main__":
    app.run()