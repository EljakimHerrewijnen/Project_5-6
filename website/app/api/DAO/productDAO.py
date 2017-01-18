from app.api.database import Database

# Get a product by id
def Find(product_id):
    db = Database()
    db.where("product_id", product_id)
    product = db.get_one("product")
    
    if not product:
        return None

    product["aromas"] = _getAroma(product["product_id"])
    return product

# Get all products
def FindAll():
    db = Database()
    sqlResult = db.get_all("product")
    if not sqlResult:
        return None
    print(sqlResult)
    for product in sqlResult:
        aromas = _getAroma(product["product_id"])
        product["aromas"] = aromas
    return sqlResult

# Get aromas for a product
def _getAroma(product_id):
    db = Database()
    db.where("product_id", product_id)
    sqlResult = db.get_all("product_aroma", "aroma_name")
    aromas = list(map(lambda row: row["aroma_name"], sqlResult))
    return aromas

# Get all products in given order
def FindByOrder(order_id):
    db = Database()
    db.join("product p", "p.product_id = od.product_id")
    db.where("orders_id", order_id)
    sqlResult = db.get_all("order_details od", "p.*, od.quantity")
    print (order_id)
    for product in sqlResult:
        aromas = _getAroma(product["product_id"])
        product["aromas"] = aromas
    return sqlResult


