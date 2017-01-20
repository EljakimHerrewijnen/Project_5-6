from app.api.database import Database
from app.api.DAO import productDAO


def Create(username, productId):
    db = Database()
    db.insert("wishes", {"username" : username, "product_id" : productId})


def Delete(username, productId):
    db = Database()
    db.where("username", username)
    db.where("product_id", productId)
    db.delete("wishes")


def FindByUser(username):
    db = Database()
    db.where("w.username", username)
    db.join("product p", "p.product_id = w.product_id")
    products = db.get_all("wishes w", "p.*")
    products = [productDAO.convert_to_json(product) for product in products]
    return products


def FindAll():
    db = Database()
    db.where("w.wishlist_public", 1)
    db.join("product p", "p.product_id = w.product_id")
    db.join("account a", "a.username = w.username")
    products = db.get_all("wishes w", "DISTINCT p.*")
    products = [productDAO.convert_to_json(product) for product in products]
    return products