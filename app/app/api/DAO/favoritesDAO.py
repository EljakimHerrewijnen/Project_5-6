from app.api.database import Database
from app.api.DAO import productDAO

# Add product to users favorits
def Create(username, product_id):
    db = Database()
    db.insert("favorites", {"username" : username, "product_id" : product_id})

# Remove product from users favorits
def Delete(username, product_id):
    db = Database()
    db.where("username", username)
    db.where("product_id", product_id)
    db.delete("favorites")

# Get all favorit products by user
def FindByUser(username):
    db = Database()
    db.where("username", username)
    db.join("product p", "p.product_id = f.product_id")
    products = db.get_all("favorites f", "p.*")
    for product in products:
        product["aromas"] = productDAO._getAroma(product["product_id"])
    return products