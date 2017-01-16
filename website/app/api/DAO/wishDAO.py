from app.api.database import Database
from app.api.DAO import productDAO

# add wish to users wishlist
def Create(username, product_id):
    db = Database()
    db.insert("wishes", {"username" : username, "product_id" : product_id})

# remove wish from users wishlist
def Delete(username, product_id):
    db = Database()
    db.where("username", username)
    db.where("product_id", product_id)
    db.delete("wishes")

# Get wishlist from user
def FindByUser(username):
    db = Database()
    db.where("w.username", username)
    db.join("product p", "p.product_id = w.product_id")
    products = db.get_all("wishes w", "p.*")
    for product in products:
        product["aromas"] = productDAO._getAroma(product["product_id"])

    return products

# get all items on a public wishlist
def FindAll():
    db = Database()
    db.where("w.wishlist_public", 1)
    db.join("product p", "p.product_id = w.product_id")
    db.join("account a", "a.username = w.username")
    products = db.get_all("wishes w", "DISTINCT p.*")
    for product in products:
        product["aromas"] = productDAO._getAroma(product["product_id"])

    return products