from flask import request
from flask import Response
from website import Models
from website import app
from flask_cors import CORS, cross_origin
from website import Database
import json

@app.route("/API/Products/<id>")
def ProductRouteHandler(id):
    # product = Models.Product.find(id)
    # return Response(product.ToJson(), mimetype='application/json')

    db = Database.Database()
    db.where("product_id", id)
    products = db.get_all("product")

    for product in products:
        db.where("product_id", product["product_id"])
        aromas = db.get_all("product_aroma", "aroma_name")
        aromaList = []
        for aroma in aromas:
            aromaList.append(aroma["aroma_name"])
        product["aromas"] = aromaList
        product["image"] = "images/{}.jpg".format(product["product_id"])
        
    return Response(db.to_jsonarray(products), mimetype='application/json')



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
        
    return Response(db.to_jsonarray(products), mimetype='application/json')


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

