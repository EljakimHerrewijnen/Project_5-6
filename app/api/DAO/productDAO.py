from app.api.database import Database

product_cache = {}
order_line_cache = {}
db = Database()
total_products = int(db.get_one("product", "COUNT(*) as c")['c'])

def convert_to_json(db_dict):
    db_dict["aromas"] = _getAroma(db_dict["product_id"])
    db_dict["roast"] = db_dict.pop("roast_level")
    db_dict["id"] = db_dict.pop("product_id")
    return db_dict


def Find(id):
    db = Database()
    if id in product_cache:
        print("RETRIEVED CACHE")
        return product_cache[id]
    db.where("product_id", id)
    product = db.get_one("product")
    product = convert_to_json(product)
    product_cache[product.id] = product
    return product


def FindAll():
    db = Database()
    if len(product_cache.items()) == total_products:
        print("RETRIEVED CACHE")
        return [value for key, value in product_cache.items()]
    products = db.get_all("product")
    products = [convert_to_json(product) for product in products]
    for value in products:
        product_cache[value['id']] = value
    return products


def _getAroma(id):
    db = Database()
    db.where("product_id", id)
    sqlResult = db.get_all("product_aroma", "aroma_name")
    aromas = list(map(lambda row: row["aroma_name"], sqlResult))
    return aromas


def FindByOrder(order_id):
    db = Database()
    if order_id in order_line_cache:
        print("RETRIEVED CACHE")
        return order_line_cache[order_id]
    db.join("product p", "p.product_id = od.product_id")
    db.where("orders_id", order_id)
    sqlResult = db.get_all("order_details od", "p.*, od.quantity")
    products = [convert_to_json(product) for product in sqlResult]
    products = [{"quantity" : product.pop('quantity'),"product" : product} for product in products]
    order_line_cache[order_id] = products
    print("DID NOT USE CACHE")
    return products