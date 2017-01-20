from app.api.database import Database
from app.api.DAO import productDAO


def Create(username, product_id):
    db = Database()
    db.insert("favorites", {"username" : username, "product_id" : product_id})


def Delete(username, productId):
    db = Database()
    db.where("username", username)
    db.where("product_id", productId)
    db.delete("favorites")


def FindByUser(username):
    db = Database()
    db.where("username", username)
    db.join("product p", "p.product_id = f.product_id")
    products = db.getAll("favorites f", "p.*")
    products = [productDAO.convert_to_json(product) for product in products]
    return products
