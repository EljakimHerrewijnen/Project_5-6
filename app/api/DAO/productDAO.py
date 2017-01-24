from app.api.database import Database


def convert_to_json(db_dict):
    db_dict["aromas"] = _getAroma(db_dict["product_id"])
    db_dict["roast"] = db_dict.pop("roast_level")
    db_dict["id"] = db_dict.pop("product_id")
    return db_dict


def Find(id):
    db = Database()
    db.where("product_id", id)
    product = db.get_one("product")
    product = convert_to_json(product)
    return product


def FindAll():
    db = Database()
    products = db.get_all("product")
    products = [convert_to_json(product) for product in products]
    return products


def _getAroma(id):
    db = Database()
    db.where("product_id", id)
    sqlResult = db.get_all("product_aroma", "aroma_name")
    aromas = list(map(lambda row: row["aroma_name"], sqlResult))
    return aromas


def FindByOrder(order_id):
    db = Database()
    db.join("product p", "p.product_id = od.product_id")
    db.where("orders_id", order_id)
    sqlResult = db.get_all("order_details od", "p.*, od.quantity")
    products = [convert_to_json(product) for product in sqlResult]
    products = [{"quantity" : product.pop('quantity'),"product" : product} for product in products]
    return products