from website.Database import Database

def Find(product_id):
    db = Database()
    db.where("product_id", product_id)
    sqlResult = db.get_one("product")
    product["aromas"] = _getAroma(product["product_id"])
    return product


def FindAll():
    db = Database()
    sqlResult = db.get_all("product") 
    for product in sqlResult:
        aromas = _getAroma(product["product_id"])
        product["aromas"] = aromas

    return sqlResult


def _getAroma(product_id):
    db = Database()
    db.where("product_id", product_id)
    sqlResult = db.get_all("product_aroma", "aroma_name")
    aromas = list(map(lambda row: row["aroma_name"], sqlResult))
    return aromas


def FindByOrder(order_id):
    db = Database()
    db.join("product p", "p.product_id = od.product_id")
    db.where("order_id", order_id)
    sqlResult = db.find_all("order_details od", "p.*, od.quantity")
    for product in sqlResult:
        aromas = _getAroma(product["product_id"])
        product["aromas"] = aromas

    return sqlResult