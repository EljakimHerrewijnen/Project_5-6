from flask import request
from flask import Response
from website import Models
from website import app
from flask_cors import CORS, cross_origin
from website import Database
import json

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

    db = Database.Database()

    products = db.get_all("product")

    for product in products:
        db.where("product_id", product["product_id"])
        aromas = db.get_all("product_aroma", "aroma_name")
        aromaList = []
        for aroma in aromas:
            aromaList.append(aroma["aroma_name"])
        product["aromas"] = aromaList
        product["image"] = "images/{}.jpg".format(product["product_id"])
        

    # if (name):
    #     products = list(filter(lambda product: product.has_name(name), products))

    # if (minPrice or maxPrice):
    #     if (minPrice and maxPrice):
    #         products = list(filter(lambda product: product.has_price(float(minPrice), float(maxPrice)), products))
    #     elif (minPrice):
    #         products = list(filter(lambda product: product.has_price(float(minPrice)), products))
    #     else:
    #         products = list(filter(lambda product: product.has_price(0, float(maxPrice)), products))
        
    # if (aromas):
    #     products = list(filter(lambda product: product.has_aromas(aromas.split(" "), True), products))

    # if (origin):
    #     products = list(filter(lambda product: product.has_origin(origin), products))

    # if (description):
    #     products = list(filter(lambda product: product.description_contains(description), products))

    # if (amount):
    #     if (offset):
    #         offset = int(offset)
    #         products = products[offset : offset + int(amount)]
    #     else:
    #         products = products[0:int(amount)]
    
    #return Response(Models.Product.ArrayToJson(products), mimetype='application/json')
    return Response(db.to_jsonarray(products), mimetype='application/json')